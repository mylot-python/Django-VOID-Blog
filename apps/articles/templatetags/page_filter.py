from django.template import Library

register = Library()

@register.filter()
def to_page_list(value):
    page = value
    page_range = page.paginator.page_range      # 当前总页数的页码列表
    last_page = page.paginator.num_pages    # 最后一页
    this_page = page.number  # 当前页

    """
    页码列表为当前页的前两页和后两页,假如page_range = [1,2,3,4,5,6]
    当前页为第1页时, page_list = [-1,0,1,2,3], 经过if x in page_range排除不存在的页码, page_list = [1,2,3]
    如当前页为第5页时, page_list = [3,4,5,6,7]
    """
    page_list = [x for x in range(this_page - 2, this_page + 3) if x in page_range]

    # 处理page_list首尾页数
    if page_list[0] - 1 >= 2:  # 判断当前第一个元素减1是否大于2
        """
        当page_list = [3,4,5,6,7], 满足page_list[0] - 1 >= 2
        page_list = ["...",3,4,5,6,7]
        """
        page_list.insert(0, "...")  # 则插入该数组成为第一个元素 ...


    if last_page - page_list[-1] >= 2:  # 判断当前最大页码数 - 列表最后一个元素相减是否大于2
        """
        当page.paginator.num_pages = 100满足条件时
        page_list = ["...",3,4,5,6,7,"..."]
        """
        page_list.append("...")  # 则添加一个元素

    if page_list[0] == "..." or page_list[0] == 2:
        """
        当满足条件时: page_list = [1,"...",3,4,5,6,7,"..."]
        """
        page_list.insert(0, 1)  # 则插入该数组成为第一个元素(首页)

    if page_list[-1] != last_page:  # 判断是否不等于最大页码
        """
        当满足条件时, 如page.paginator.num_pages=100: page_list = [1,"...",3,4,5,6,7,"...",100]
        """
        page_list.append(last_page)  # 不等于则插入到最后一个元素(尾页)

    return page_list



@register.filter()
def to_banner_list(value):
    page = value
    page_range = page.get('page_list')      # 当前总页数的页码列表
    last_page = page.get('max_page')       # 最后一页
    this_page = page.get('this_page')    # 当前页

    """
    页码列表为当前页的前两页和后两页,假如page_range = [1,2,3,4,5,6]
    当前页为第1页时, page_list = [-1,0,1,2,3], 经过if x in page_range排除不存在的页码, page_list = [1,2,3]
    如当前页为第5页时, page_list = [3,4,5,6,7]
    """
    page_list = [x for x in range(this_page - 2, this_page + 3) if x in page_range]

    # 处理page_list首尾页数
    if page_list[0] - 1 >= 2:  # 判断当前第一个元素减1是否大于2
        """
        当page_list = [3,4,5,6,7], 满足page_list[0] - 1 >= 2
        page_list = ["...",3,4,5,6,7]
        """
        page_list.insert(0, "...")  # 则插入该数组成为第一个元素 ...


    if last_page - page_list[-1] >= 2:  # 判断当前最大页码数 - 列表最后一个元素相减是否大于2
        """
        当page.paginator.num_pages = 100满足条件时
        page_list = ["...",3,4,5,6,7,"..."]
        """
        page_list.append("...")  # 则添加一个元素

    if page_list[0] == "..." or page_list[0] == 2:
        """
        当满足条件时: page_list = [1,"...",3,4,5,6,7,"..."]
        """
        page_list.insert(0, 1)  # 则插入该数组成为第一个元素(首页)

    if page_list[-1] != last_page:  # 判断是否不等于最大页码
        """
        当满足条件时, 如page.paginator.num_pages=100: page_list = [1,"...",3,4,5,6,7,"...",100]
        """
        page_list.append(last_page)  # 不等于则插入到最后一个元素(尾页)

    return page_list
