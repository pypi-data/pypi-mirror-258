import setuptools  
  
# 指定要打包的目录  
PACKAGE_DIR = 'yunxiaoapi'  # 请替换为你的目录名  
  
# 设置打包的元数据  
setuptools.setup(  
    name="yunxiaoapi",  # 请替换为你的包名
    author="YKM",
    author_email="18678617683@163.com",
    description="基于云校数字平台的身份校验库",
    version="0.0.1",
    url="http://tbstxl.wikidot.com/",
    packages=setuptools.find_packages(where=PACKAGE_DIR),  
    install_requires=['requests',],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
