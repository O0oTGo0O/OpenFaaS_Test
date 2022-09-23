import DobotDllType as dType
import time

CON_STR = {
    dType.DobotConnect.DobotConnect_NoError:  "DobotConnect_NoError",
    dType.DobotConnect.DobotConnect_NotFound: "DobotConnect_NotFound",
    dType.DobotConnect.DobotConnect_Occupied: "DobotConnect_Occupied"}

#将dll读取到内存中并获取对应的CDLL实例
#Load Dll and get the CDLL object
api = dType.load()
#建立与dobot的连接
#Connect Dobot
state = dType.ConnectDobot(api, "", 115200)[0]
print("Connect status:",CON_STR[state])

if (state == dType.DobotConnect.DobotConnect_NoError):
    print('success')

    dType.SetQueuedCmdClear(api)
    # 返回机械臂坐标
    print(dType.GetPose(api))
    print(dType.GetHOMEParams(api))

    # 手持示教
    dType.SetHHTTrigOutputEnabled(api, isEnabled=1)


    # 获取六个位置，分别为抓取位置， 识别位置， RGB颜色分拣位置和初始位置
    i = 0
    while i < 6:
        if dType.GetHHTTrigOutput(api)[0]:
            if i == 0:
                grab_x, grab_y, grab_z, grab_r, j1, j2, j3, j4 = dType.GetPose(api)
            if i == 1:
                rec_x, rec_y, rec_z, rec_r, j1, j2, j3, j4 = dType.GetPose(api)
            if i == 2:
                red_x, red_y, red_z, red_r, j1, j2, j3, j4 = dType.GetPose(api)
            if i == 3:
                green_x, green_y, green_z, green_r, j1, j2, j3, j4 = dType.GetPose(api)
            if i == 4:
                blue_x, blue_y, blue_z, blue_r, j1, j2, j3, j4 = dType.GetPose(api)
            if i == 5:
                init_x, init_y, init_z, init_r, j1, j2, j3, j4 = dType.GetPose(api)
            i += 1

    dType.SetInfraredSensor(api, isEnable=1, infraredPort=dType.InfraredPort.PORT_GP4)
    dType.SetColorSensor(api, isEnable=1, colorPort=dType.ColorPort.PORT_GP2, version=1)

    dType.SetEMotor(api, index=0, isEnabled=1, speed=5000, isQueued=1)
    dType.SetQueuedCmdStartExec(api)
    dType.SetQueuedCmdStopExec(api)
    while True:
        if dType.GetInfraredSensor(api,dType.InfraredPort.PORT_GP4)[0] == 1:
            dType.SetQueuedCmdClear(api)
            lastIndex = dType.SetEMotor(api, index=0, isEnabled=0, speed=0, isQueued=1)[0]
            lastIndex = dType.SetPTPCmd(api, dType.PTPMode.PTPJUMPXYZMode, grab_x, grab_y, grab_z, grab_r, isQueued=1)[0]
            lastIndex = dType.SetEndEffectorSuctionCup(api, enableCtrl=1, on=1, isQueued=1)[0]
            lastIndex = dType.SetWAITCmd(api, 1000, isQueued=1)[0]
            lastIndex = dType.SetPTPCmd(api, dType.PTPMode.PTPJUMPXYZMode, rec_x, rec_y, rec_z, rec_r, isQueued=1)[0]
            lastIndex = dType.SetWAITCmd(api, 1000, isQueued=1)[0]

            # 开始执行指令队列
            # Start to Execute Command Queue
            dType.SetQueuedCmdStartExec(api)

            # 如果还未完成指令队列则等待
            # Wait for Executing Last Command
            while lastIndex > dType.GetQueuedCmdCurrentIndex(api)[0]:
                dType.dSleep(100)
            # 停止执行指令
            # Stop to Execute Command Queued
            dType.SetQueuedCmdStopExec(api)

            # 清空
            dType.SetQueuedCmdClear(api)
            color = dType.GetColorSensor(api)
            print(color)
            if color.index(max(color)) == 0:
                lastIndex = dType.SetPTPCmd(api, dType.PTPMode.PTPJUMPXYZMode, red_x, red_y, red_z, red_r, isQueued=1)[0]
            elif color.index(max(color)) == 1:
                lastIndex = dType.SetPTPCmd(api, dType.PTPMode.PTPJUMPXYZMode, green_x, green_y, green_z, green_r, isQueued=1)[0]
            elif color.index(max(color)) == 2:
                lastIndex = dType.SetPTPCmd(api, dType.PTPMode.PTPJUMPXYZMode, blue_x, blue_y, blue_z, blue_r, isQueued=1)[0]
            lastIndex = dType.SetEndEffectorSuctionCup(api, enableCtrl=1, on=0, isQueued=1)[0]
            lastIndex = dType.SetPTPCmd(api, dType.PTPMode.PTPJUMPXYZMode, init_x, init_y, init_z, init_r, isQueued=1)[0]
            lastIndex = dType.SetEMotor(api, index=0, isEnabled=1, speed=5000, isQueued=1)[0]

            # 开始执行指令队列
            # Start to Execute Command Queue
            dType.SetQueuedCmdStartExec(api)

            # 如果还未完成指令队列则等待
            # Wait for Executing Last Command
            while lastIndex > dType.GetQueuedCmdCurrentIndex(api)[0]:
                dType.dSleep(100)

            # 停止执行指令
            # Stop to Execute Command Queued
            dType.SetQueuedCmdStopExec(api)

#断开连接
#Disconnect Dobot
dType.DisconnectDobot(api)
