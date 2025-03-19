# GPT3.5 Autonomous Driving Motion Planning
This is a course project for ECS289G Advance NLP.

Contributor: Hanchu Zhou, and Chreyl Ngai.

## Introduction
We propose a novel approach that leverages the power of LLMs for motion planning in autonomous driving. Motion planning involves devising safe and optimal driving trajectories for autonomous vehicles in diverse scenarios while accounting for unpredictable human behaviors and environmental factors. We propose to reformulate motion planning as a language modeling problem, representing heterogeneous inputs as language tokens and utilizing LLMs’ reasoning capability to generate waypoint coordinates for future driving trajectories. With the help of LLMs, the results can include explanations in natural language that illustrate the model’s motivation of each critical behavior. Our approach demonstrates the ability of the LLM to forecast highly reasonable trajectories with an average collision rate of 1.4% with very limited number of examples (111), successfully completing the required driving distance while fulfilling the task goals. It shows the LLM's strong potential capacity in planning.

## Data Collection
We use the CARLA autonomous driving simulation platform to generate training data. We introduce a novel rule-based collision-free planning algorithm. At its core, the algorithm takes a destination as input and embarks on a two-tiered planning process. Initially, it employs the A* algorithm for global route planning, establishing a path to the destination while considering the static map environment. Then the local planning phase refines this path into a smooth trajectory suitable for real-time navigation. Upon detecting an obstacle within the lane, the algorithm strategically calculates a new temporary destination to facilitate lane changing, thus enabling the vehicle to overtake the obstacle safely and efficiently.

<p align="center">
  <img width="260" alt="co" aline="center" src="https://github.com/cherylcy/llm-motion-planner/assets/55656554/fe637e36-695b-4406-97a4-d448b3f746ff">
</p>

To validate our algorithm and facilitate data collection for further analysis, we construct a specific scenario within the CARLA platform. This scenario simulates a four-lane highway environment peppered with randomly placed stationary vehicles acting as obstacles. Each simulation run randomizes the location of these obstacle vehicles, ensuring a wide variety of encounter scenarios. The primary objective for the ego vehicle, under these conditions, is to navigate forward towards a predetermined destination while avoiding collisions with any obstacle vehicles.

<p align="center">
  <img width="260" alt="scenario" src="https://github.com/cherylcy/llm-motion-planner/assets/55656554/f4ef4f3b-d6f9-42e7-8bd9-1e9bf0e65436">
  <img width="260" alt="sc2" src="https://github.com/cherylcy/llm-motion-planner/assets/55656554/c723e834-14d7-428e-860f-c811b9561a1c">
</p>

We record the locations and dimensions of obstacle vehicles as inputs for the LLM. Each trajectory executed by the ego vehicle, in response to the dynamic scenario configurations, is recorded as output data. This iterative process generates a comprehensive dataset. The data is then inserted into to the natural language prompt template.

<p align="center">
  <img width="600" alt="sample_input_styled" src="https://github.com/cherylcy/llm-motion-planner/assets/55656554/cbdfc90f-f8e1-4900-be42-a6dddf66be67">
</p>


## Experiments
We employ OpenAI’s GPT-3.5-turbo model as the motion planner due to its strong reasoning capabilities. The generated dataset contains 136 samples of collision-free trajectories with the corresponding environment setting. We split the whole dataset into training and validation sets, comprising 111 and 25 samples respectively. The training set is utilized to fine-tune GPT-3.5-turbo model for four epochs. We then evaluate the performance on the validation set using three metrics: L1 error, collision rate, and success rate. The table below shows the model’s performance after fine-tuning for 1, 3, and 4 epochs.

<p align="center">
  <img width="300" alt="eval_stat" src="https://github.com/cherylcy/llm-motion-planner/assets/55656554/905105af-6844-43bc-92e7-63b467b97f07">
</p>

An example predicted trajectory after 1, 3, and 4 epochs of fine-tuning:

<p align="center">
  <img width="600" alt="prediction21" src="https://github.com/cherylcy/llm-motion-planner/assets/55656554/004faf1f-e859-437b-88d4-8fa5d25d27b8">
</p>

