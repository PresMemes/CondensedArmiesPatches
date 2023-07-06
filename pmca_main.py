from pmca_multiplier import pmca_multiplyOp
from pmca_inserter import pmca_insertOp

# Args: Input file name and/or path, Output file name and/or path, converting from x10 -> x100, the prefix the mod uses (set to something weird if there isn't one used)
InsertOperation = pmca_insertOp("input.txt", "output.txt", False)

# Args: Input file name and/or path, Output file name and/or path, converting from x10 -> x100
MultiplyOperation = pmca_multiplyOp("input.txt", "output.txt", False)

# Args: Input file name and/or path, Output file name and/or path, converting from x10 -> x100
MultiplyOperationp2 = pmca_multiplyOp("input.txt", "output.txt", True)

# InsertOperation.readAndWrite -> Check for errors and update pmca_materiel_policy_check -> MultiplyOperation.readAndWrite() -> MultiplyOperationp2.readAndWrite()
#InsertOperation.readAndWrite()
#MultiplyOperation.readAndWrite()
MultiplyOperationp2.readAndWrite()
