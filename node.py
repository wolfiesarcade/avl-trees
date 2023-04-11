class Node:
    def __init__(self, value, parent=None, left=None, right=None, height=1):
        self.value = value
        self.left = left
        self.right = right
        self.parent = parent
        self.height = height

    def display(self, show_heights=False):
        res = ''
        lines, *_ = self._display_aux(show_heights)
        for line in lines:
            res += line + '\n'
        return res

    def __str__(self):
        return str(self.value)

    def _display_aux(self, show_heights=False):
            """Returns list of strings, width, height, and horizontal coordinate of the root."""
            if show_heights:
                node_description = f'{self.value}:{self.height}'
            else:
                node_description = f'{self.value}'
                
            # No child.
            if self.right is None and self.left is None:
                line = node_description
                width = len(line)
                height = 1
                middle = width // 2
                return [line], width, height, middle

            # Only left child.
            if self.right is None:
                lines, n, p, x = self.left._display_aux(show_heights)
                s = node_description
                u = len(s)
                first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s
                second_line = x * ' ' + '/' + (n - x - 1 + u) * ' '
                shifted_lines = [line + u * ' ' for line in lines]
                return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

            # Only right child.
            if self.left is None:
                lines, n, p, x = self.right._display_aux(show_heights)
                s = node_description
                u = len(s)
                first_line = s + x * '_' + (n - x) * ' '
                second_line = (u + x) * ' ' + '\\' + (n - x - 1) * ' '
                shifted_lines = [u * ' ' + line for line in lines]
                return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2

            # Two children.
            left, n, p, x = self.left._display_aux(show_heights)
            right, m, q, y = self.right._display_aux(show_heights)
            s = node_description
            u = len(s)
            first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s + y * '_' + (m - y) * ' '
            second_line = x * ' ' + '/' + (n - x - 1 + u + y) * ' ' + '\\' + (m - y - 1) * ' '
            if p < q:
                left += [n * ' '] * (q - p)
            elif q < p:
                right += [m * ' '] * (p - q)
            zipped_lines = zip(left, right)
            lines = [first_line, second_line] + [a + u * ' ' + b for a, b in zipped_lines]
            return lines, n + m + u, max(p, q) + 2, n + u // 2
