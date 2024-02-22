import os

import duckdb
import ibis
import typer

from infra.pg_proxy.server import create as create_pg_proxy
from vinyl.lib.definitions import load_project_defs
from vinyl.lib.metric import MetricStore
from vinyl.lib.project import Project

project_cli = typer.Typer(pretty_exceptions_show_locals=False)


@project_cli.command("deploy")
def deploy():
    """Deploy a Vinyl project"""
    defs = load_project_defs()
    if not os.path.exists(".vinyl"):
        os.makedirs(".vinyl")
    if os.path.exists(".vinyl/vinyl.duckdb"):
        os.remove(".vinyl/vinyl.duckdb")

    conn = ibis.duckdb.connect(".vinyl/vinyl.duckdb")
    project = Project(resources=defs.resources, models=defs.models)
    for model in project.models:
        table = model()
        if isinstance(table, MetricStore):
            # we dont support this yet
            continue

        conn.create_table(model.__name__, table.execute().to_pyarrow())


@project_cli.command("serve")
def serve():
    """Serve a Vinyl project"""
    bv_host = "0.0.0.0"
    bv_port = 5433
    if not os.path.exists(".vinyl/vinyl.duckdb"):
        raise RuntimeError("No database found in .vinyl/vinyl.duckdb")

    conn = duckdb.connect(".vinyl/vinyl.duckdb")
    print("(Turntable) Using DuckDB database at .vinyl/vinyl.duckdb")
    print("(Turntable) Tables:")
    tables = conn.execute("show tables;").fetchall()
    for table in tables:
        print(f"- {table[0]}")
    server = create_pg_proxy(conn, (bv_host, bv_port))
    ip, port = server.server_address
    print(f"\nListening on {ip}:{port}")
    try:
        server.serve_forever()
    finally:
        server.shutdown()
        conn.close()
