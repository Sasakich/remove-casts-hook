import clang.cindex


def remove_redundant_casts(file_path):
    index = clang.cindex.Index.create()
    tu = index.parse(file_path)

    with open(file_path, 'r') as f:
        code_lines = f.readlines()

    for node in tu.cursor.walk_preorder():
        if node.kind == clang.cindex.CursorKind.CSTYLE_CAST_EXPR:
            cast_type = node.type.spelling
            operand = list(node.get_children())[0]
            operand_type = operand.type.spelling

            if cast_type == operand_type:
                start_line = node.extent.start.line - 1
                start_column = node.extent.start.column - 1
                end_column = node.extent.end.column - 1

                code_lines[start_line] = code_lines[start_line][:start_column] + code_lines[start_line][end_column:]

    with open(file_path, 'w') as f:
        f.writelines(code_lines)