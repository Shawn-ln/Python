"""
Python3 数据结构
"""
"""
列表
Python中列表是可变的，这是它区别于字符串和元组的最重要的特点，一句话概括即：列表可以修改，而字符串和元组不能。
以下是 Python 中列表的方法：

方法	              描述
list.append(x)	把一个元素添加到列表的结尾，相当于 a[len(a):] = [x]。
list.extend(L)	通过添加指定列表的所有元素来扩充列表，相当于 a[len(a):] = L。
list.insert(i, x)	在指定位置插入一个元素。第一个参数是准备插入到其前面的那个元素的索引，例如 a.insert(0, x) 会插入到整个列表之前，而 a.insert(len(a), x) 相当于 a.append(x) 。
list.remove(x)	删除列表中值为 x 的第一个元素。如果没有这样的元素，就会返回一个错误。
list.pop([i])	从列表的指定位置移除元素，并将其返回。如果没有指定索引，a.pop()返回最后一个元素。元素随即从列表中被移除。（方法中 i 两边的方括号表示这个参数是可选的，而不是要求你输入一对方括号，你会经常在 Python 库参考手册中遇到这样的标记。）
list.clear()	移除列表中的所有项，等于del a[:]。
list.index(x)	返回列表中第一个值为 x 的元素的索引。如果没有匹配的元素就会返回一个错误。
list.count(x)	返回 x 在列表中出现的次数。
list.sort()	对列表中的元素进行排序。
list.reverse()	倒排列表中的元素。
list.copy()	返回列表的浅复制，等于a[:]。
注意：类似 insert, remove 或 sort 等修改列表的方法没有返回值。
下面示例演示了列表的大部分方法：
"""
# a = [66.25, 333, 333, 1, 1234.5]
# print(a.count(333), a.count(66.25), a.count('x'))
# a.insert(2, -1)
# a.append(333)
# print('append', a, a.count(333))
# a.index(333)
# a.remove(333)
# print('remove', a)
# a.reverse()
# print('reverse', a)
# a.sort()
# print('sort', a)
# -----------------------------------------------
"""
将列表当做堆栈使用
列表方法使得列表可以很方便的作为一个堆栈来使用，堆栈作为特定的数据结构，最先进入的元素最后一个被释放（后进先出）。
用 append() 方法可以把一个元素添加到堆栈顶。用不指定索引的 pop() 方法可以把一个元素从堆栈顶释放出来。例如：
"""
# stack = [3, 4, 5]
# stack.append(6)
# stack.append(7)
# print(stack)
# stack.pop()
# print(stack)
# stack.pop()
# print(stack)
# stack.pop()
# print(stack)
# -----------------------------------------------
"""
将列表当作队列使用
也可以把列表当做队列用，只是在队列里第一加入的元素，第一个取出来；但是拿列表用作这样的目的效率不高。在列表的最后添加或者弹出元素速度快，
然而在列表里插入或者从头部弹出速度却不快（因为所有其他的元素都得一个一个地移动）。
"""
# from collections import deque
# queue = deque(["Eric", "John", "Michael"])
# queue.append("Terry")
# queue.append("Graham")
# print(queue)
# queue.popleft()
# print(queue)
# queue.popleft()
# print(queue)
# -----------------------------------------------
"""
列表推导式
列表推导式提供了从序列创建列表的简单途径。通常应用程序将一些操作应用于某个序列的每个元素，用其获得的结果作为生成新列表的元素，
或者根据确定的判定条件创建子序列。
每个列表推导式都在 for 之后跟一个表达式，然后有零到多个 for 或 if 子句。返回结果是一个根据表达从其后的 for 和 if 上下文环
境中生成出来的列表。如果希望表达式推导出一个元组，就必须使用括号。
这里我们将列表中每个数值乘三，获得一个新的列表：
"""
# vec = [2, 4, 6]
# print([3 * x for x in vec])
# print([[x, x**2] for x in vec])
# print([[x, x*3] for x in vec if x > 3])
# print([[x, x*3] for x in vec if x < 3])
# -----------------------------------------------
"""
这里我们对序列里每一个元素逐个调用某方法：
"""
# freshfruit = ['  banana', '  loganberry', 'passion fruit   ']
# print([weapon.strip() for weapon in freshfruit])     # strip 返回原字符串的副本，删除前导和末尾的空格。
# -----------------------------------------------
"""
以下是一些关于循环和其它技巧的演示：
"""
# vec1 = [2, 4, 6]
# vec2 = [4, 3, -9]
# print([x * y for x in vec1 for y in vec2])
# print([x + y for x in vec1 for y in vec2])
# print([vec1[i] + vec2[i] for i in range(len(vec1))])
# """
# 列表推导式可以使用复杂表达式或嵌套函数：
# """
# print([str(round(355/113, i)) for i in range(1, 6)])
# print(str(round(355/113, 4)))   # 将一个数字四舍五入到十进制数字的给定精度。
# -----------------------------------------------
"""
嵌套列表解析
Python的列表还可以嵌套。
以下实例将3X4的矩阵列表转换为4X3列表：
"""
# matrix = [
#     [1, 2, 3, 4],
#     [5, 6, 7, 8],
#     [9, 10, 11, 12],
# ]
# print([[row[i] for row in matrix] for i in range(4)])
# """
# 另外一种实现方法
# """
# transposed = []
# for i in range(4):
#     # the following 3 lines implement the nested listcomp
#     transposed_row = []
#     for row in matrix:
#         transposed_row.append(row[i])
#         print(transposed_row)
#     transposed.append(transposed_row)
#     print(transposed)
"""
    [1]
    [1, 5]
    [1, 5, 9]
    [[1, 5, 9]]
    [2]
    [2, 6]
    [2, 6, 10]
    [[1, 5, 9], [2, 6, 10]]
    [3]
    [3, 7]
    [3, 7, 11]
    [[1, 5, 9], [2, 6, 10], [3, 7, 11]]
    [4]
    [4, 8]
    [4, 8, 12]
    [[1, 5, 9], [2, 6, 10], [3, 7, 11], [4, 8, 12]]
"""
# -----------------------------------------------
"""
del 语句
使用 del 语句可以从一个列表中依索引而不是值来删除一个元素。这与使用 pop() 返回一个值不同。
可以用 del 语句从列表中删除一个切割，或清空整个列表（我们以前介绍的方法是给该切割赋一个空列表）。例如：
"""
# a = [-1, 1, 66.25, 333, 333, 1234.5]
# print(a)
# del a[0]
# print(a)
# del a[2:4]
# print(a)
# del a[:]
# print(a)
# -----------------------------------------------
"""
元组和序列
元组在输出时总是有括号的，以便于正确表达嵌套结构。在输入时可能有或没有括号， 不过括号通常是必须的（如果元组是更大的表达式的一部分）。
元组由若干逗号分隔的值组成，例如：
"""
# t = 12345, 54321, 'hello'
# print(t)
# u = t, (1, 2, 3, 4, 5)
# print(u)
# -----------------------------------------------