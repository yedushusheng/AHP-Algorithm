import rhinoscriptsyntax as rs

# 创建函数生成民居结构
def create_house(length, width, height, num_bedrooms, num_bathrooms):
    # 创建矩形地基
    base_plane = rs.WorldXYPlane()
    base = rs.AddRectangle(base_plane, length, width)

    # 创建两层结构
    floor_height = height / 2
    second_floor_height = height - floor_height

    # 创建第一层
    first_floor = rs.AddBox(base_plane, length, width, floor_height)

    # 创建第二层
    second_floor = rs.AddBox(base_plane, length, width, second_floor_height)
    second_floor_translate = rs.VectorCreate((0, 0, floor_height), (0, 0, 0))
    rs.MoveObject(second_floor, second_floor_translate)

    # 分隔房间
    bedroom_width = length / 2
    bedroom_length = width / (num_bedrooms + 1)
    bathroom_width = length / 4
    bathroom_length = width / (num_bathrooms + 1)

    # 创建卧室和洗手间
    for i in range(num_bedrooms):
        bedroom_x = bedroom_length * (i + 1)
        bedroom_rect = rs.AddRectangle(base_plane, bedroom_width, bedroom_length, 0)
        bedroom_translate = rs.VectorCreate((bedroom_x, 0, 0), (0, 0, 0))
        rs.MoveObject(bedroom_rect, bedroom_translate)

    for i in range(num_bathrooms):
        bathroom_x = bathroom_length * (i + 1)
        bathroom_rect = rs.AddRectangle(base_plane, bathroom_width, bathroom_length, 0)
        bathroom_translate = rs.VectorCreate((bathroom_x, width - bathroom_length, 0), (0, 0, 0))
        rs.MoveObject(bathroom_rect, bathroom_translate)

    return base, first_floor, second_floor

# 调用函数创建民居结构
length = 20
width = 8
height = 8
num_bedrooms = 2
num_bathrooms = 1

create_house(length, width, height, num_bedrooms, num_bathrooms)
