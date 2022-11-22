import setuptools

# Setup the markdown
readme_markdown = ""
ignore = False
for l in open("README.md"):
    if l.startswith("[HTMLElementBegin]"):
        ignore = True
        continue
    elif l.startswith("[HTMLElementEnd]"):
        ignore = False
        continue
    else:
        readme_markdown += l if not ignore else ""
        
# Setup the requirements
requirements = []
for l in open("requirements.txt"):
    requirements.append(l.strip())

setuptools.setup(
    name='wormhole-streaming',
    version="1.0.0",
    description='Simple and Hackable Realtime Video Streaming Engine',
    author='Edward Li',
    url='https://github.com/RadioactiveHydra/Wormhole/',
    python_requires='>=3.9',
    packages=['wormhole', 'wormhole.streamer', 'wormhole.video', 'wormhole.viewer', 'wormhole.assets'],
    package_data={'wormhole.assets':['*']},
    install_requires=requirements,
    long_description=readme_markdown,   
    long_description_content_type='text/markdown',
    project_urls={
        "Source Code": "https://github.com/RadioactiveHydra/Wormhole",
        "Bug Reports": "https://github.com/RadioactiveHydra/Wormhole/issues",
        "Demo": "https://demo.wormhole.hydranet.dev/",
        "Discord": "https://discord.gg/9QF2bPc",
    }
)
