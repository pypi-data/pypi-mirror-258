class parse:
    def __init__(self,sfzh_id:str,check:bool=True,parse_area:bool=True):
        message="参数必须是一个长度为18的字符串（中国公民身份证号码）！字符串前17位必须为数字，最后一位为'X'或数字!"
        if not len(sfzh_id)==18:
            del self
            raise Exception(message)
        
        try:
            self.area_code=sfzh_id[0:6]    #地区代码
            int(self.area_code)
            self.sheng_code=sfzh_id[0:2]
            int(self.sheng_code)
            self.shi_code=sfzh_id[2:4]
            int(self.shi_code)
            self.xian_code=sfzh_id[4:6]
            int(self.xian_code)
            
            self.year=int(sfzh_id[6:10])    #生日
            self.month=int(sfzh_id[10:12])
            self.day=int(sfzh_id[12:14])
            self.date=sfzh_id[6:14]
            
            self.serial=int(sfzh_id[14:16])
            
            if int(sfzh_id[16])%2==0:   #性别
                self.gender="female"
            else:
                self.gender="male"
            
            if sfzh_id[17]=="x" or sfzh_id[17]=="X":    #校验码
                self.check_code="X"
            else:
                self.check_code=int(sfzh_id[17])
            
        except:
            del self
            raise Exception(message)

        if check==True:
            self.check_result=generate(sfzh_id)

        if parse_area==True:
            pass
            
                     
def generate(sfzh_id:str):
    weights = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]  
    codes = ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2']  
      
    sum_of_products = sum(int(sfzh_id[i]) * weights[i] for i in range(17))  #乘积求和 
    remainder = sum_of_products % 11    #对11取模
    code=codes[remainder] #获取校验码

    if len(sfzh_id)==18:
        sfzh_id=sfzh_id.upper()
        if sfzh_id[17]==code:
            return True
        else:
            return False
    elif len(sfzh_id)==17:
        return code
    else:
        raise Exception("参数错误！")
        
   

if __name__=="__main__":
    s=parse(input())
    print(s.sheng_code,s.shi_code,s.xian_code,s.year,s.month,s.day,s.date,s.serial,s.gender,s.check_code,s.check_result)
