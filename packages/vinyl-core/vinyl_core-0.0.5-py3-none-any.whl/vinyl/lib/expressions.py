import ibis
import ibis.expr.types as ir


def case(
    pairs: list[tuple[ir.BooleanValue, ir.Value]], default: ir.Value | None = None
) -> ir.Value:
    if len(pairs) == 0:
        raise ValueError("At least one pair must be provided")
    elif len(pairs) == 1:
        return ibis.ifelse(pairs[0][0], pairs[0][1], default)

    out = ibis.case()
    for pair in pairs:
        out = out.when(pair[0], pair[1])
    out = out.else_(default)
    return out.end()


def if_else(
    condition: ir.BooleanValue, true_value: ir.Value, false_value: ir.Value
) -> ir.Value:
    return ibis.ifelse(condition, true_value, false_value)
