class Solution:
    def reverseList(self, head):
        cur = head   
        pre = None
        while(cur!=None):
            temp = cur.next # 保存一下 cur的下一个节点，因为接下来要改变cur->next
            cur.next = pre #反转
            #更新pre、cur指针
            pre = cur
            cur = temp
        return pre

    def reverseList(self, head):
        cur = head
        pre = None
        while(cur!=None):
            temp = cur.next
            cur.next = pre
            pre = cur
            cur = temp
        return pre