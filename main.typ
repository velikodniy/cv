#import "template.typ": *


#show: curriculum-vitae.with(
  author: "Vadim Velicodnii",
  positions: ("Tech Lead", "Machine Learning", "DevOps", "Full-Stack"),
  contacts: (
    email: "vadim.velikodniy@gmail.com",
    github: "velikodniy",
    linkedin: "vadim-velicodnii"
  )
)

= Experience

#job(
  position: "Senior Machine Learning Engineer",
  company: "Snap",
  location: "London, UK",
  date: "Oct 2018 --- now",
)[
  - Tech lead and key developer of the Snap AI (formerly, SnapML Kit) core parts: infrastructure, backend, frontend, integrations with internal services and ML pipelines.
    One of the authors of the app idea (Patent #link("https://patents.google.com/patent/WO2023230064A1")[WO2023230064A1])
    - #link("https://ar.snap.com/snapml-kit")[Snap AI] is a no/low-code web application for creating ML-powered lenses, 3D resources, generate videos, etc.
    - Cross-team collaboration: various ML teams, Snap infrasturture, lens designers, Lens Studio developers, monetization, production & infrastructure security, privacy and legal.
    - Impact:
      - The internal version of the app is being used for 2+ years for developing viral ML lenses boosting user engagement.
      - GenAI Suite backed by Snap AI is one the main Lens Studio features #link("https://newsroom.snap.com/sps-2024-new-ai-powered-tools")[announced] during Snap Partner Summit 2024.
    - Tech stack: Python, FastAPI, PostgreSQL, Temporal, Kubernetes, Terraform, Google Cloud, TypeScript, React, etc.
  - Worked on the deep learning technologies behind Snap's first ML lenses.
    - One of the authors of the novel DL model used for creating the lenses. (Patent #link("https://patents.google.com/patent/US11900565B2")[US11900565B2])
    - Since at that time (2018---2019) many modern models didn't exist, this project required a lot of research and development.
    - Impact:
      - The lenses became viral and boosted financial metrics.
    Tech stack: PyTorch, CUDA, various DL models and techniques.
  - Empowered ML lens development by creating pipelines, data lakes, tools, CUDA kernels, libraries, bindings and integrations.
    - Impact:
      - The dataset prepared by me were the crucial part of the ML training pipelines.
      - Automation allowed running multiple experiemnts efficiently and release new effects more often than before.
    - Tech stack: Python, C++, Rust, CUDA, GLSL.
  - Leadership:
    - Established development processes in the team.
    - Prepared style and developement guides, introduced best development practices, encouraged other by example.
    - Regularly gave tech talks to familiarize the team with new technologies.
    - Prepared a lot of documentation.
    - Onboarded and mentored new team members.
]

#job(
  position: "Senior Machine Learning Specialist",
  company: "Teleport Future Technologies",
  location: "Remote",
  date: "Oct 2016 --- Apr 2018",
)[
  - Research and development in deep learning and computer vision.
    - Novel deep learning architecture for real-time on-device segmentation.
    - Realistic colorization.
  - Developed:
    - GUI tools for the designers and developers.
    - Deep learning framwork for fast iteration over model designs.
    - Web platform for partners to test the models on the server side.
    - Demo Android app.
  - Tech stack: Python, TensorFlow, Qt, AWS, GLSL, Android, Java, CUDA.
]

#job(
  position: "Senior Lecturer",
  company: "Shevchenko Transnistria State University",
  location: "Tiraspol, Moldova",
  date: "Sep 2006 --- Sep 2018",
)[
  - Gave lectures on software development and design, algorithms, machine learning, systems programming, numerical analysis, CFD, etc.
  - Supervised 10+ diploma theses.
  - Won the Presidential Award "Best Young University Lecturer".
  - Research and development in computational fluid dynamics, deep learning, evolutionary algorithms.
]

= Education

// TODO: implement #uni
#job(
  position: "Applied Mathematics and Computer Science",
  company: "Shevchenko Transnistria State University",
  date: "Sep 2001 --- Jun 2006")[
    - Specialist degree (with honor)
    - GPA: 4.9 / 5.0
]

= Skills

#skill("Languages", (strong("English"), "Russian"))

// Volunteering
// Certifications
