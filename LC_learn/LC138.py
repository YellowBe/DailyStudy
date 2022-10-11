# 138. 复制带随机指针的链表
# 给你一个长度为 n 的链表，每个节点包含一个额外增加的随机指针 random ，该指针可以指向链表中的任何节点或空节点。

# 构造这个链表的 深拷贝。 深拷贝应该正好由 n 个 全新 节点组成，其中每个新节点的值都设为其对应的原节点的值。新节点的 next 指针和 random 指针也都应指向复制链表中的新节点，并使原链表和复制链表中的这些指针能够表示相同的链表状态。复制链表中的指针都不应指向原链表中的节点 。

# 例如，如果原链表中有 X 和 Y 两个节点，其中 X.random --> Y 。那么在复制链表中对应的两个节点 x 和 y ，同样有 x.random --> y 。

# 返回复制链表的头节点。

# 用一个由 n 个节点组成的链表来表示输入/输出中的链表。每个节点用一个 [val, random_index] 表示：

# val：一个表示 Node.val 的整数。
# random_index：随机指针指向的节点索引（范围从 0 到 n-1）；如果不指向任何节点，则为  null 。
# 你的代码 只 接受原链表的头节点 head 作为传入参数。

class Solution(object):
    def copyRandomList(self, head):
        if not head:
            return None
        p = head
        # 第一步， 在每个原节点后面创建一个新节点
        # 1->1'->2->2'->3->3'
        while p:
            new_node = Node(p.val, None, None)
            new_node.next = p.next
            p.next = new_node
            p = new_node.next
        p = head
        # 第二步，设置新节点的随机节点
        while p:
            if p.random:
                p.next.random = p.random.next #p.next是p的复制节点， 那么p的复制节点的random就指向p的random该指向的地方
            p = p.next.next
        # 第三步, 将两个链表分离
        p = head
        dummy = Node(-1, None, None)
        cur = dummy
        while p:
            cur.next = p.next
            cur = cur.next
            p.next = cur.next
            p = p.next
        return dummy.next

# 用hash表来创建
class Solution(object):
    def copyRandomList(self, head):
        if not head:
            return None
        # 创建一个哈希表,key 是原节点， value是新节点
        d = dict()
        p = head
        while p:
            new_node = Node(p.val,None,None)
            d[p] = new_node
            p = p.next
        p = head
        while p:
            if p.next:
                d[p].next = d[p.next]
            if p.random:
                d[p].random = d[p.random]
            p = p.next
        return d[head]