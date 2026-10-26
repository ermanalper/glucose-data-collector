from datetime import datetime, timezone
from typing import Optional

from sympy import Poly, Rational, Symbol, interpolate

from app.core.ports.repositories.glucose_repository_interface import IGlucoseRepository
from app.core.ports.repositories.interpolation_repository_interface import IInterpolationRepository
from app.models.poly_result import PolyResult
from app.services.interfaces.foresee_glucose_service_interface import IForeseeGlucoseService


class ForeseeGlucoseService(IForeseeGlucoseService):
    def __init__(self, interpolation_repo: IInterpolationRepository, glucose_repo: IGlucoseRepository):
        self._glucose_repo = glucose_repo
        self._interpolation_repo = interpolation_repo
        self._running = False

    def interpolate(self, start_time: datetime, end_time: datetime, user_id: str = "default_user") -> Optional[PolyResult]:
        if self._running:
            print("Another interpolation calculation is running")
            return None
        self._running = True

        try:
            print('Interpolation starts')
            # get the glucose data between the start time and the end time
            data = self._glucose_repo.get_by_time_interval(
                user_id=user_id, start=start_time, end=end_time
            )

            if not data:
                return PolyResult(coefficients=[], degree=0)

            # sort time (most probably already sorted but do it anyway, this will not run frequently) and normalize
            sorted_data = sorted(
                data,
                key=lambda g: (
                    g.timestamp.replace(tzinfo=timezone.utc)
                    if g.timestamp.tzinfo is None
                    else g.timestamp.astimezone(timezone.utc)
                ),
            )

            t0 = (
                sorted_data[0].timestamp.replace(tzinfo=timezone.utc)
                if sorted_data[0].timestamp.tzinfo is None
                else sorted_data[0].timestamp.astimezone(timezone.utc)
            )

            # use Rational to eliminate errors such as roundoff or truncation
            points_by_x: dict[Rational, Rational] = {}
            for g in sorted_data:
                ts = (
                    g.timestamp.replace(tzinfo=timezone.utc)
                    if g.timestamp.tzinfo is None
                    else g.timestamp.astimezone(timezone.utc)
                )
                delta = ts - t0
                total_microseconds = (delta.days * 86400 + delta.seconds) * 1_000_000 + delta.microseconds
                x_exact = Rational(total_microseconds, 1_000_000)
                points_by_x[x_exact] = Rational(g.value)

            points = list(points_by_x.items())
            if len(points) == 1:
                return PolyResult(coefficients=[float(points[0][1])], degree=0)

            x_sym = Symbol("x")
            lagrange_expr = interpolate(points, x_sym)
            poly = Poly(lagrange_expr, x_sym)

            coeffs = [float(c) for c in poly.all_coeffs()]

            poly_result = PolyResult(coefficients=coeffs, degree=(len(coeffs) - 1))
            self._interpolation_repo.save_interpolation(poly_result, timestamp=datetime.now(timezone.utc))
            print('Interpolation ends')
            return poly_result
        finally:
            self._running = False



