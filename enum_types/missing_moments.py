"""How μ, Σ, and PSR N treat NaNs in incomplete X."""

from enum import StrEnum


class MissingMoments(StrEnum):
    """Pairwise vs complete-case moments. Does **not** drop the row from ŷ.

    Incomplete ``X`` rows still receive ``r = NaN`` and prediction weight 0.
    This enum only picks μ / Σ / PSR ``N``.

    Names match MATLAB ``corr`` / ``corrcoef`` ``'Rows'`` (``'pairwise'`` /
    ``'complete'``), not ``'omitrows'``.
    """

    PAIRWISE = "pairwise"
    COMPLETE = "complete"

    def drop_na(self) -> bool:
        """``True`` when average / nancov should use listwise complete-case."""
        return self is MissingMoments.COMPLETE

    @classmethod
    def parse(cls, value) -> "MissingMoments":
        """Accept the enum, ``"pairwise"`` / ``"complete"``, and bool aliases.

        ``False`` / ``0`` / ``"false"`` → pairwise. ``True`` / ``1`` /
        ``"true"`` / ``"listwise"`` → complete.
        """
        if isinstance(value, cls):
            return value
        if value is None:
            return cls.PAIRWISE
        if isinstance(value, bool) or value in (0, 1):
            return cls.COMPLETE if value else cls.PAIRWISE
        s = str(value).strip().lower()
        if s in ("pairwise", "false", "0"):
            return cls.PAIRWISE
        if s in ("complete", "true", "1", "listwise"):
            return cls.COMPLETE
        raise ValueError(
            f"missing_moments must be 'pairwise' or 'complete'; got {value!r}"
        )
