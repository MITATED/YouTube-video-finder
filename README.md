# Valuable-YouTube-Video-Finder
*Made on the basis https://github.com/chris-lovejoy/YouTube-video-finder. 
## The project
The purpose of this project is to enable users to find valuable YouTube videos of their interest independent of YouTube's recommendation system. For a more detailed explanation of the project, it's purpose and how it was made, see this [post on Medium](https://towardsdatascience.com/i-created-my-own-youtube-algorithm-to-stop-me-wasting-time-afd170f4ca3a).

## Setup

### YouTube-API-Key
You will need to acquire a YouTube v3 API key, which you can do so easily [here](https://console.developers.google.com/cloud-resource-manager). A helpful video outlining the process can be found [here](https://www.youtube.com/watch?v=-QMg39gK624). After receiving the API key, specify it as the API_KEY environment variable.

### Packages
All requirements are contained within [requirements.txt](https://github.com/mitated/YouTube-video-finder/blob/master/requirements.txt).

To install them, execute the following from the root directory:
```
pip install -r requirements.txt
```

## Execution

### Local
After configuring config.yaml and installing requirements, the function can be executed from the command line using:

```
python3 lambda_function.py 'search term 1' 'search term 2'
```

The default search period is 7 days, but this can be modified with the '--search-period' argument.

For example:

```
python3 lambda_function.py 'machine learning' 'medical school' --search-period 10
```

This will call the [**lambda_function.py function**](https://github.com/mitated/YouTube-video-finder/blob/master/main.py) and output will be printed into the console.

### Lambda
You can run the script `./deploy_to_lambda`. It will create a virtual environment and archive it along with the source files of the program. Then it will immediately upload this as source code into a function on AWS Lambda called YouTube (in the script you can change the name)


