import DobotDllType as dType
import time

CON_STR = {
    dType.DobotConnect.DobotConnect_NoError: "DobotConnect_NoError",
    dType.DobotConnect.DobotConnect_NotFound: "DobotConnect_NotFound",
    dType.DobotConnect.DobotConnect_Occupied: "DobotConnect_Occupied"}

# 将dll读取到内存中并获取对应的CDLL实例
# Load Dll and get the CDLL object
api = dType.load()
# 建立与dobot的连接
# Connect Dobot
state = dType.ConnectDobot(api, "", 115200)[0]
print("Connect status:", CON_STR[state])

if (state == dType.DobotConnect.DobotConnect_NoError):
    print('success')
    dType.SetQueuedCmdClear(api)
    print(dType.GetQueuedCmdCurrentIndex(api))

    print(dType.GetDeviceVersionEx(api))
    lastIndex = dType.SetEMotor(api, index=0, isEnabled=0, speed=5000, isQueued=1)[0]
    print(lastIndex)
    lastIndex = dType.SetEndEffectorSuctionCup(api, enableCtrl=0, on=1, isQueued=1)[0]
    dType.SetInfraredSensor(api, isEnable=0, infraredPort=dType.InfraredPort.PORT_GP4)
    dType.SetColorSensor(api, isEnable=0, colorPort=dType.ColorPort.PORT_GP2, version=1)
    print(lastIndex)
    # dType.SetQueuedCmdStopExec(api)

    # 开始执行指令队列
    # Start to Execute Command Queue
    dType.SetQueuedCmdStartExec(api)

    # 如果还未完成指令队列则等待
    # Wait for Executing Last Command
    while lastIndex > dType.GetQueuedCmdCurrentIndex(api)[0]:
        print(lastIndex)
        dType.dSleep(100)
    # 停止执行指令
    # Stop to Execute Command Queued
    dType.SetQueuedCmdStopExec(api)



# 断开连接
# Disconnect Dobot
dType.DisconnectDobot(api)
