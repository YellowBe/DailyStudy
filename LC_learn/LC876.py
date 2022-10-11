class Solution:
    def middleNode(self, head):
        if not head or not head.next: return head
        
        slow, fast = head, head
        while fast.next and fast.next.next:
            slow, fast = slow.next, fast.next.next
        
        if fast.next == None: return slow
        return slow.next
    def middleNode(self, head):
        if not head or not head.next: return head
        slow, fast = head, head
        while fast.next and fast.next.next:
            slow, fast = slow.next, fast.next.next
        if fast.next == None: return slow
        return slow.next
    def middleNode(self, head):
        if not head or not head.next: return head
        slow, fast = head, head
        while fast.next and fast.next.next:
            slow, fast = slow.next, fast.next.next
        if fast.next == None: return slow
        return slow.next