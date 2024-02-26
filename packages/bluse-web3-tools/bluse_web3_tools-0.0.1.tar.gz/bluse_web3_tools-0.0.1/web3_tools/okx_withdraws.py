# Hx@831121
# apikey = "a609da30-9605-4a01-ad1c-f2b03ea011e3"
# secretkey = "9BBCE5CA45C4E213DD63E082F2702446"
# IP = ""
# 备注名 = "zk1"
# 权限 = "读取/提现"
import okx.Funding as Funding

api_key = "a609da30-9605-4a01-ad1c-f2b03ea011e3"
secret_key = "9BBCE5CA45C4E213DD63E082F2702446"
passphrase = "Hx@831121"


addrs = []
addrs.append('0x1C3Ab4068337A13533246b3e6ac226BdE74579cb')
addrs.append('0x6Ac744d52f231D783afe39ede9ca06B225cfAc47')
addrs.append('0xcc043630cFBF573B883176958B7697063e485F8c')
addrs.append('0x237495282322D868D750ec0f89e5D7D10d6115C0')
addrs.append('0x777Ab233363E80dBDf07927B5DEadFAD39EEc6c3')
addrs.append('0x3eA120470d65E2d3DE1D7628FC38cF79098F22fA')
addrs.append('0x20ffDB110Cd767099bb1F916a21f54c123a0accB')
addrs.append('0x81402133CC9f14A6742cBBbEc17749Fd68451276')
addrs.append('0xe7c942Ec03E8712304abd0bF8CC6e2A757b6922D')
addrs.append('0x0412BDbE3f84a27A201dbA3Ca1832a8e63a3D8d7')
addrs.append('0x1Fe60420227899cb93F60B28AD25bD1F29C5506d')
addrs.append('0xC75c24E3a4A467cB4b77c81Ed76EC493418CB1Ca')
addrs.append('0x5fdE95832626061cFd56Ab85a75e906f5dA194bb')
addrs.append('0xd398fd3585653945D459696Ba9cf734098411544')
addrs.append('0xE5f9fbBfdcde3a4C07a4780E32124B4D9003F69d')
addrs.append('0x0150d7e1003191461D1960344b7b8B488DdDA6D8')
addrs.append('0x9f476bbb47EB0C4123998ba38d02B4169bf46F6C')
addrs.append('0xEC3DE5AB1F25EE8c574F3f51Ee296Febd9902868')
addrs.append('0xcBA745f38B964652A15081720bFb5bCC887d8b3D')
addrs.append('0x5953aF8612619edF21511633a28191e3C769cF6f')
addrs.append('0xf75E0096194e37E4B56680723922037D38FBA84e')
addrs.append('0x1577A18381F3180a13612D8938d890dEa818e436')
addrs.append('0xab28EEb0B563b29491c88B7DC363Cb57e0C31b5c')
addrs.append('0xbd8af484DA4A679e5050b56254CF758F15d8D7cF')
addrs.append('0xf3Cd2fC967e7E118a1Eb2cae13CD849Fb370a398')
addrs.append('0x7DB1414A1C5f7E944bCb9FbE3741f88c12Eca7Bd')
addrs.append('0xAB29d24Ec6f8BA7C4805F1D1892fC55220495B7e')
addrs.append('0xB6aa35b3E2EF570eCA16ab9d27E6E66C99AfF187')
addrs.append('0x2Aa9dDf1dF79a69fD3d9C73B94298cdA2D98683E')
addrs.append('0x0C8F59C4e685deE4085311Bb3A88aA8E877533de')



for toAddr in addrs:
    flag = "0"  # live trading: 0, demo trading: 1
    ccy = 'MATIC'
    amt = '3.5'
    dest = '4'
    fee = '0.48'
    chain = 'MATIC-Polygon' #ETH-zkSync Era

    fundingAPI = Funding.FundingAPI(api_key, secret_key, passphrase, False, flag)
    result = fundingAPI.withdrawal(ccy, amt, dest, toAddr, fee, chain)
    print(result)
