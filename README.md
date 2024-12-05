# EasyRDW-Local

EasyRDW 是一个轻量级的 RDW 算法测试框架，用户可以方便地在其上实现 RDW 方法，并即时看到自己算法的表现。

[Easy RDW-Web](https://github.com/MoonstoneF/EasyRDW-Web)

## 1. 安装
1. 将仓库克隆到本地；

2. 安装所需依赖；

```
pip install -r requirements.txt
```

## 2. 使用

### 2.1 编写 RDW 控制器

你只需要实现 RDW 核心算法，框架将帮你处理其他事情。具体地，你需要至少在 `controller/client_logic.py` 中实现 `calc_gain` 函数和 `update_reset` 函数。非必要不应修改 `client_base.py` 和 `utils` 目录下的文件。

`calc_gain` 负责在每一帧根据当前物理空间状态计算应应用的 gain 值。其输入为当前时刻的用户状态、物理空间情况以及当前帧时长，输出为三个 gain 值和旋转方向：平移增益、旋转增益、曲率增益半径，以及使用曲率增益时的物理转向方向（1 或 -1，1 代表顺时针，-1代表逆时针）。

`update_reset` 只有在需要重置时才会被触发，输入为**碰撞前一刻**的用户状态、物理空间信息和当前帧时长，输出为重置后的用户状态。

`controller/client_logic.py` 中已有一个样例实现。该实现在用户行进过程中总采用建议的最大平移增益和旋转增益，并不尝试弯曲用户行走路径。重置时该实现采用简单的 2-1 Turn 策略，让用户在虚拟空间中旋转一周的同时在物理空间中旋转 180 度。可以尝试更改其中不同参数的值以对这些 gain 值如何工作有一个直观的认识。

### 2.2 运行

为与网页端对接，你需要先启动：

```
python client_base.py
```

然后按照 [Easy RDW-Web](https://github.com/MoonstoneF/EasyRDW-Web) 项目中的提示启动服务器，访问网页端，在左侧的 Control Panel 打开 Local 面板即可。如果网页在点击 START 按钮后仍然没有响应，可能需要重启本地端、刷新网页等。

### 2.3 其它

我们用五元组 `(x,y,angle,v,w)` 表示物理空间中的用户状态。其中 `(x,y)` 为用户在物理空间中的坐标，`angle` 为用户在物理空间中的朝向（弧度制），`v` 为用户在虚拟空间中的速度（也是用户**认为**自己在物理空间中的速度），`w` 为用户在虚拟空间中的角速度（也是用户**认为**自己在物理空间中的角速度）。

表示物理空间时，我们用 `border` 表示其边界多边形，并有一个 `obstacle_list` 表示全体障碍物。每个障碍物都是一个多边形。

在命令行参数中，你可以通过 `-f` 选项自定义你的控制器文件位置，而不是默认的 `controller/client_logic.py`。

此外，你还可以通过 `-u` 选项启用**通用接口模式**。在这种模式下，你不再需要实现 `calc_gain` 函数，而是需要实现一个 `update_user` 函数。这个函数接受当前用户状态、物理空间和帧长度作为输入，直接返回下一帧的用户状态。通用接口模式还支持主动重置。你可以查看 `controller/client_logic_universal.py` 中实现的 `update_user` 函数作为参考。

所有待实现函数的例子可以在 `controller/client_logic.py` 中找到。对一切可能用到的类的定义，请参考 `utils/space.py` 中的相关内容。此外 `utils/misc.py` 封装了一个对实现通用接口可能有用的函数；`utils/constants.py` 定义了几个常见参数的值。

## 3. 提示

### 3.1 常见错误提示

- 无法打开网页：建议检查是否严格按 [Easy RDW-Web](https://github.com/MoonstoneF/EasyRDW-Web) 的步骤启动本地服务器。如果仍然无法打开网页，建议尝试换一个端口或开全局代理。

- 网页显示 `Local not connected! Start the Local WebSocket server and refresh this page.`：没有连接上 `client_base.py` 建立的 Websocket Server，建议检查是否打开 Websocket，是否因为一些不当操作使得 Websocket 连接错误关闭等。
- 算法更新后，测试时却依然调取旧算法：建议重启 `client_base.py`。如果仍然出现这个问题，建议尝试换一个端口。
- 测试时卡在墙里出不来：建议检查 reset 逻辑是否实现恰当。如果确保自己的 reset 实现没有问题但依然出现卡墙，可向课程助教反馈相关情况。

注意：本项目只是一个 RDW 算法的测试框架，因此为方便实现与可视化，本框架中的算法依据用户状态直接操纵用户在物理空间中的行动。在真实 VR 应用中使用 RDW 算法的时候，应获取到用户状态后以此修改虚拟空间中用户看到自身的行动。

### 3.2 重定向行走简介

RDW（Redirected Walking）重定向行走技术通过轻微地改变用户在虚拟环境中的行走方向，使他们在现实世界中走更少的距离，而在虚拟环境中却能覆盖更大的区域。这样，用户可以在有限的物理空间内体验到更大的虚拟空间。

RDW 技术的基本原理是利用人类视觉系统对方向感知的不精确性。当用户在虚拟环境中行走时，系统会根据用户的行走方向和速度，适当地调整虚拟环境中的方向等，使现实世界中的行走路径与虚拟世界中的行走路径产生偏差。这种偏差在现实世界中是微小的，但在虚拟世界中却可以放大，甚至实现无限行走的效果。

人体感知的不精确性在 RDW 中用增益（gain）值衡量。平移增益、旋转增益和曲率增益是三种常见的增益值。

- 平移增益（Translation Gain）：
平移增益是指用户在现实世界中行走时，虚拟环境中对应的平移距离的比例。例如，如果平移增益设置为 2，那么用户在现实世界中走 1 米，在虚拟环境中就会看到自己平移了 2 米。平移增益可以用来扩大或缩小虚拟环境中的空间感，使用户能够在有限的物理空间内探索更大的虚拟空间。`constant.py` 中建议的平移增益范围为 $[0.86,1.26]$，研究表明这个范围内的平移增益是不容易被用户察觉的。

- 旋转增益（Rotation Gain）：
旋转增益是指用户在现实世界中旋转时，虚拟环境中对应的旋转角度的比例。例如，如果旋转增益设置为 1.5，那么用户在现实世界中旋转 30 度，在虚拟环境中就会看到自己旋转了 45 度。旋转增益可以用来调整用户在虚拟环境中的方向感知，使其与现实世界中的方向保持一致或产生偏差，从而实现 RDW 的效果。建议的旋转增益范围为 $[0.67,1.24]$。

- 曲率增益（Curvature Gain）：
曲率增益往往用曲率增益半径衡量，这是指用户在虚拟空间中走直线的时候，在物理空间中走的曲线的半径。例如，如果曲率增益半径设置为 10 米，那么用户在虚拟空间中走直线的时候，在物理空间中就会走一个半径为 10 米的圆弧。曲率增益可以用来调整用户在虚拟环境中的行走路径，使其与现实世界中的行走路径产生偏差。建议的曲率增益半径为至少 $7.5m$。

灵活使用这三种 gain 值就足以设计出效果非常优秀的 RDW 方法。也有一些方法采用了这些之外的 gain 值类型。

可供参考的相关综述和若干 RDW 方法论文：

- [15 Years of Research on Redirected Walking in Immersive Virtual Environments](https://ieeexplore.ieee.org/document/8255772)

- [A Comprehensive Review of Redirected Walking Techniques Taxonomy, Methods, and Future Directions](https://link.springer.com/article/10.1007/s11390-022-2266-7)

- [Redirected Walking for Exploring Immersive Virtual Spaces with HMD : A Comprehensive Review and Recent Advances](https://ieeexplore.ieee.org/document/9785918)

- [Overcoming Spatial Constraints in VR: A Survey of Redirected Walking Techniques](https://link.springer.com/article/10.1007/s11390-024-4585-3)

- S2O, S2C, S2MT: [Comparing Four Approaches to Generalized Redirected Walking: Simulation and Live User Data](https://ieeexplore.ieee.org/document/6479192)

- APF: [A General Reactive Algorithm for Redirected Walking Using Artificial Potential Functions](https://ieeexplore.ieee.org/document/8797983)

- SRL: [A Reinforcement Learning Approach to Redirected Walking with Passive Haptic Feedback](https://ieeexplore.ieee.org/document/9583811)
- OPG-RDW: [Optimal Pose Guided Redirected Walking with Pose Score Precomputation](https://ieeexplore.ieee.org/document/9756797)
