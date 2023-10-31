# Policy on adding new images and packages

There are many things we consider, while adding new images and packages.

Here is a non exhaustive list of things we do care about:

1. **Software health**, details, and maintenance status
   - reasonable versioning is adopted, and the version is considered to be stable
   - has been around for several years
   - the package maintains documentation
   - a changelog is actively maintained
   - a release procedure with helpful automation is established
   - multiple people are involved in the maintenance of the project
   - provides a `conda-forge` package besides a `pypi` package, where both are kept up to date
   - supports both `x86_64` and `aarch64` architectures
2. **Installation consequences**
   - GitHub Actions build time
   - Image sizes
   - All requirements should be installed as well
3. Jupyter Docker Stacks _**image fit**_
   - new package or stack is changing (or inherits from) the most suitable stack
4. **Software impact** for users of docker-stacks images
   - How this image can help existing users, or maybe reduce the need to build new images
5. Why it shouldn't just be a documented **recipe**
6. Impact on **security**
   - Does the package open additional ports, or add new web endpoints, that could be exploited?

With all this in mind, we have a voting group, which consists of
[mathbunnyru](https://github.com/mathbunnyru),
[consideRatio](https://github.com/consideRatio),
[yuvipanda](https://github.com/yuvipanda) and
[manics](https://github.com/manics).

This voting group is responsible for accepting or declining new packages and stacks.
The change is accepted, if there are **at least 2 positive votes**.
