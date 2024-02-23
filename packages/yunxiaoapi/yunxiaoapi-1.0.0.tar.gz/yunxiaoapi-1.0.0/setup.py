import setuptools  
  
# 设置打包的元数据  
setuptools.setup(  
    name="yunxiaoapi",  # 请替换为你的包名
    author="ykm",
    author_email="18678617683@163.com",
    description="基于云校数字平台的身份校验库",
    version="1.0.0",
    packages=setuptools.find_packages(),  
    install_requires=['requests'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3'
    ]
)
