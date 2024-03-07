
import rhinoscriptsyntax as rs

# 这里展示了一个简单的房屋设计的例子
def create_house(length, width, height):
    # 创建矩形地基
    base_plane = rs.WorldXYPlane()
    corners = [(0, 0, 0), (length, 0, 0), (length, width, 0), (0, width, 0)]
    base = rs.AddSrfPt(corners)

    # 创建房屋立面
    height = rs.AddBox(rs.WorldXYPlane(), length, width, height)

    # 将立面移至地基顶部
    translation_vector = (0, 0, height)
    rs.MoveObject(height, translation_vector)

    return base, height

# 在Rhino界面上执行Python脚本，调整参数
base, height = create_house(20, 15, 10)
