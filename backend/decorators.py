# def fence(func):
#     def wrapper(text: str):
#         print("")
#         func()
#         print("+" * 25)
#     return wrapper

def custom_fence(fence: str = "+"):
    def add_fence(func):
        def wrapper(text: str):
            print(fence * len(text))
            func(text)
            print(fence * len(text))
        return wrapper
    return add_fence

@custom_fence("-")
def log(text:str):
    print(text)

log("Hello, World!")