chieuCaoToiThieu = 150
chieuCaoToiDa = 200 
canNangToiThieu = 40
canNangToiDa = 100

chieuCaoTB = (chieuCaoToiThieu + chieuCaoToiDa) / 2
canNangTB = (canNangToiThieu + canNangToiDa) / 2

class XacSuat:
    def __init__(self):
        self.thap = 0
        self.trungbinh = 0
        self.cao = 0

class Size:

    def size(self, chieuCao, canNang):
        self.S = 0
        self.M = 0
        self.L = 0    
        self.X = 0
        self.XL = 0
        self.XXL = 0

        result = ketQua(chieuCao, canNang) 
        
def xac_suat(c_chieuCao, c_canNang, chieuCao, canNang):
    if chieuCao < chieuCaoToiThieu:
       c_chieuCao.thap = 1
    elif chieuCao >= canNangToiThieu and chieuCao < chieuCaoTB:
        c_chieuCao.trungbinh = 2 * (chieuCao - chieuCaoToiThieu) / (chieuCaoToiDa - chieuCaoToiThieu)
        c_chieuCao.thap = 1 - c_chieuCao.trungbinh
    elif chieuCao >= chieuCaoTB and chieuCao <= chieuCaoToiDa:
        c_chieuCao.cao = 2 * (chieuCaoToiDa - chieuCao) / (chieuCaoToiDa - chieuCaoToiThieu)
        c_chieuCao.binh_thuong = 1 - c_chieuCao.cao
    elif chieuCao >= chieuCaoToiDa:
        c_chieuCao.cao = 1

    if canNang < canNangToiThieu:
       c_canNang.thap = 1
    elif canNang >= canNangToiThieu and canNang < canNangTB:
        c_canNang.trungbinh = 2 * (canNang - canNangToiThieu) / (canNangToiDa - canNangToiThieu)
        c_canNang.thap = 1 - c_canNang.trungbinh
    elif canNang >= canNangTB and canNang <= canNangToiDa:
        c_canNang.cao = 2 * (canNangToiDa - canNang) / (canNangToiDa - canNangToiThieu)
        c_canNang.binh_thuong = 1 - c_canNang.cao
    elif canNang >= canNangToiDa:
        c_canNang.cao = 1    
       
def ketQua(chieuCao, canNang):
        
    c_chieuCao = XacSuat()
    c_canNang = XacSuat()
    xac_suat(c_chieuCao, c_canNang, chieuCao, canNang)
    size = Size()
    size.S = (max(min(c_chieuCao.thap,c_canNang.thap),min(c_chieuCao.thap,c_canNang.trungbinh)))
    size.M = (max(min(c_chieuCao.trungbinh, c_canNang.thap), min(c_chieuCao.thap,c_canNang.cao)))
    size.L = (max(min(c_chieuCao.trungbinh, c_canNang.trungbinh), min(c_chieuCao.trungbinh,c_canNang.cao)))
    size.X = (min(c_chieuCao.cao,c_canNang.thap))
    size.XL = (min(c_chieuCao.cao,c_canNang.trungbinh))
    size.XXL = (min(c_chieuCao.cao,c_canNang.cao))

    probabilityMax = max(size.S,size.M,size.L,size.X,size.XL,size.XXL)

    if probabilityMax == size.S:
        return "Size S và số đo quần của bạn có thể là 27, 28, 29 tùy thuộc vào độ rộng của bụng"
    elif probabilityMax == size.M:
        return "Size M và số đo quần của bạn có thể là 28, 29, 30 tùy thuộc vào độ rộng của bụng"
    elif probabilityMax == size.L:
        return "Size L và số đo quần của bạn có thể là 29, 30, 31 tùy thuộc vào độ rộng của bụng"
    elif probabilityMax == size.X:
        return "Size X và số đo quần của bạn có thể là 30, 31, 32 tùy thuộc vào độ rộng của bụng"
    elif probabilityMax == size.XL:
        return "Size XL và số đo quần của bạn có thể là 31, 32, 33 tùy thuộc vào độ rộng của bụng"
    else:
        return "Size XXL và số đo quần của bạn có thể là 32, 33, 34 tùy thuộc vào độ rộng của bụng"        