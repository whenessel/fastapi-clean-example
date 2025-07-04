from line_profiler import LineProfiler

from app.domain.value_objects.raw_password.raw_password import RawPassword
from app.infrastructure.adapters.password_hasher_bcrypt import (
    BcryptPasswordHasher,
    PasswordPepper,
)


def run_operations(hasher: BcryptPasswordHasher) -> None:
    raw_password = RawPassword("raw_password")
    hashed = hasher.hash(raw_password)
    hasher.verify(raw_password=raw_password, hashed_password=hashed)


def setup_profiler() -> tuple[LineProfiler, BcryptPasswordHasher]:
    hasher = BcryptPasswordHasher(PasswordPepper("Cayenne!"))
    profiler = LineProfiler()

    profiler.add_function(hasher.hash)
    profiler.add_function(hasher.verify)
    profiler.add_function(run_operations)

    return profiler, hasher


def main() -> None:
    profiler, hasher = setup_profiler()
    profiler.runcall(run_operations, hasher)  # type: ignore[no-untyped-call]
    profiler.print_stats()


if __name__ == "__main__":
    main()
