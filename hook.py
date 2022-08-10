import time

class LazyPerson(object):
    def __init__(self, name):
        self.name = name
        self.watch_tv_func = None
        self.have_dinner_func = None

    def get_up(self):
        print("%s get up at:%s" % (self.name, time.time()))

    def go_to_sleep(self):
        print("%s go to sleep at:%s" % (self.name, time.time()))

    def register_tv_hook(self, watch_tv_func):
        self.watch_tv_func = watch_tv_func

    def register_dinner_hook(self, have_dinner_func):
        self.have_dinner_func = have_dinner_func

    def enjoy_a_lazy_day(self):

        # get up
        self.get_up()
        time.sleep(0.1)
        # watch tv
        # check the watch_tv_func(hooked or unhooked)
        # hooked
        if self.watch_tv_func is not None:
            self.watch_tv_func(self.name)
        # unhooked
        else:
            print("no tv to watch")
        time.sleep(0.1)
        # have dinner
        # check the have_dinner_func(hooked or unhooked)
        # hooked
        if self.have_dinner_func is not None:
            self.have_dinner_func(self.name)
        # unhooked
        else:
            print("nothing to eat at dinner")
        time.sleep(0.1)
        self.go_to_sleep()

def watch_daydayup(name):
    print("%s : The program ---day day up--- is funny!!!" % name)

def watch_happyfamily(name):
    print("%s : The program ---happy family--- is boring!!!" % name)

def eat_meat(name):
    print("%s : The meat is nice!!!" % name)


def eat_hamburger(name):
    print("%s : The hamburger is not so bad!!!" % name)


class ContentStash(object):  
    """  
    content stash for online operation  
    pipeline is  
    1. input_filter: filter some contents, no use to user  
    2. insert_queue(redis or other broker): insert useful content to queue  
    """  
  
    def __init__(self):  
        self.input_filter_fn = None  
        self.broker = []  
  
    def register_input_filter_hook(self, input_filter_fn):  
        """  
        register input filter function, parameter is content dict  
        Args:  
            input_filter_fn: input filter function  
  
        Returns:  
  
        """  
        self.input_filter_fn = input_filter_fn  
  
    def insert_queue(self, content):  
        """  
        insert content to queue  
        Args:  
            content: dict  
  
        Returns:  
  
        """  
        self.broker.append(content)  
  
    def input_pipeline(self, content, use=False):  
        """  
        pipeline of input for content stash  
        Args:  
            use: is use, defaul False  
            content: dict  
  
        Returns:  
  
        """  
        if not use:  
            return  
  
        # input filter  
        if self.input_filter_fn:  
            _filter = self.input_filter_fn(content)  
              
        # insert to queue  
        if not _filter:  
            self.insert_queue(content)  
  
  
  
# test  
## 实现一个你所需要的钩子实现：比如如果content 包含time就过滤掉，否则插入队列  
def input_filter_hook(content):  
    """  
    test input filter hook  
    Args:  
        content: dict  
  
    Returns: None or content  
  
    """  
    if content.get('time') is None:  
        return  
    else:  
        return content  
  
  
# 原有程序  
content = {'filename': 'test.jpg', 'b64_file': "#test", 'data': {"result": "cat", "probility": 0.9}}  
content_stash = ContentStash('audit', '')  
  
# 挂上钩子函数， 可以有各种不同钩子函数的实现，但是要主要函数输入输出必须保持原有程序中一致，比如这里是content  
content_stash.register_input_filter_hook(input_filter_hook)  
  
# 执行流程  
content_stash.input_pipeline(content)  
  


# if __name__ == "__main__":
#     lazy_tom = LazyPerson("Tom")
#     lazy_jerry = LazyPerson("Jerry")
#     # register hook
#     lazy_tom.register_tv_hook(watch_daydayup)
#     lazy_tom.register_dinner_hook(eat_meat)
#     lazy_jerry.register_tv_hook(watch_happyfamily)
#     lazy_jerry.register_dinner_hook(eat_hamburger)
#     # enjoy a day
#     lazy_tom.enjoy_a_lazy_day()
#     lazy_jerry.enjoy_a_lazy_day()