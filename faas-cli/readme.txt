该文件夹下是在搭建openfaas平台中一些函数的底层实现

每一个文件夹（除了build 和 template外）都是一个函数的具体实现

具体打包、部署方法可参考 《openfass环境搭建.pdf》

其中较为方便用于测试的函数为：add（字符串）
输入：1,2,3,4,5,6
输出：21

数组函数：seq（包含sort,cut和reverse）
输入：
{
  "function": "sort",
  "array": [1,3,4,0,4,3,1],
  "method":"descend" 
}

{
  "function": "cut",
  "array": [1,3,4,0,4,3,1],
  "n":"3" 
}