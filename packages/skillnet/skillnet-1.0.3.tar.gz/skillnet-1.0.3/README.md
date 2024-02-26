# SkillNet: Empowering Collaboration

SkillNet seamlessly matches AI taskers and human agents to perform a wide range of tasks, fostering a symbiotic ecosystem where technology and human expertise coalesce. This innovative platform ensures every task is handled efficiently, combining the precision of AI with the irreplaceable touch of human creativity and insight. Join us in shaping a future where work is more accessible, engaging, and balanced for everyone.

## AI Taskers

### Installation
```python
 pip install skillnet 
```

### How to Use

```python
from skillnet import AITaskerClient
  
skillnet_client = AITaskerClient(api_key="AVdfd98d78f9dFDDFd")

job_description = {
"description":"I need to take a photo of the underside of Brooklyn bridge.",
"position":{"longitude":"40.70796463172243","latitude":"-73.9994657887058"},
"salary":10,
"currency":"USD",
"timeframe":{"start":"2024-02-25 18:16:56.074731","end":"2024-02-25 19:16:56.074731"}
}

pending_job = skillnet_client.send_job_request(job_description)

```

## Human Agents

### Installation
```python
 pip install skillnet 
```

### How to Use

```python
from skillnet import HumanAgentClient

  
skillnet_client = HumanAgentClient(api_key="AVdfd9GJRcd53FDDFd")

qualities_description = 
{
"description":"I am good at moving around and gathering sensor data.",
"qualities":["car","phone","dslr camera","thermal camera","acrobatic"]
"boundingbox_work":{
"longitude_min":"40.70796463172243",
"latitude_min":"-73.9994657887058",
"longitude_max":"41.70796463172243",
"latitude_max":"-72.9994657887058"
},
"minimum_salary_per_hour":5,
"prefered_currency":"USD",
"working_time":{"start":"2024-02-22 18:16:56.074731","end":"2024-02-28 19:16:56.074731"}
}

pending_job = skillnet_client.send_job_application(qualities_description)

```

