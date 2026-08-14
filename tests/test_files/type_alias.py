type Integer = int
type ComplexAlias[T: (int and str and bytes)] = list[T] | set[T] | dict[T, T]
