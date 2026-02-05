# resusew

resusew is an automatic resume tailoring util. divide your
resume into components, and let the script choose the best ones
for a given job description!

the main problem resusew aims to solve is space. you may find
that all your skills and experience cant fit on one page, which
isnt ideal. if you include everything, then your resume becomes
diluted by irrelevant content. even if everything fits, you
want your most relevant skills and experience to appear first.
resusew solves both of these issues by putting the most relevant
content first, and omitting everything else, such that
everything fits on a single page

resusew also provides some advantages over ai tailoring tools:
- ai-generated content isnt perfect, and generally requires
proof-reading, which can be time consuming. resusew doesnt have
this issue, because all of the content is written by you
- ai is expensive to run, and so many tools out there come with
a subscription cost. running a local model can be cheaper, but
is still overkill for simply tailoring a resume, and you still
run into the issue of having to proof-read its output

## installation

clone the repo
```
git clone https://github.com/BenLee8602/resusew.git resusew
cd resusew
```

### prod

for general use, use `pipx` to install resusew as a cli tool.
see below for usage
```
pipx install .
```

### dev

for developers, install dependencies and run
```
pip install -r requirements.txt
python -m resusew args...
```

run tests using pytest
```
pytest
```

## usage

resusew takes two inputs: a resusew template, a job
description. it resolves the template for the given job, and
outputs the tailored resume. see below for info about the
resusew template format, and how to resusew-ify your resume

run resusew via terminal
```
resusew resume.xyz.resusew jobdesc.txt resume.xyz
```
where:
- `resume.xyz.resusew` input file name (resusew template)
- `jobdesc.txt` file containing job description
- `resume.xyz` output file name (tailored resume)

## getting started

heres how you can modify your existing document to be used with
resusew. for this example, our resume will be written in the
LaTeX format, but resusew will work with any plain-text format

```tex
\textbf{Distributed Chat Platform}

Personal Project |
\href{linkToGithub}{\underline{GitHub}} |
\href{linkToWebsite}{\underline{Website}}

\begin{itemize}
    \item Built a real-time chat application using WebSockets and Node.js
    \item Implemented horizontal scaling with Redis pub/sub and Docker
    \item Designed a PostgreSQL schema for message persistence and search
    \item Created a React frontend with optimistic UI updates
    \item Added authentication, presence tracking, and typing indicators
    \item Deployed the system to Kubernetes with automated CI/CD
\end{itemize}
```
here is a snippet from our resume, showing one of our personal
projects. the problem is that its too long! we have other
projects on our resume, not to mention our skills, experience,
and education sections. our resume ends up being more than one
page, which isnt ideal. we can use resusew to fix this

```diff
\textbf{Distributed Chat Platform}

Personal Project |
\href{linkToGithub}{\underline{GitHub}} |
\href{linkToWebsite}{\underline{Website}}

\begin{itemize}
+__RESUSEW_BEG__ real-time,websockets,node
    \item Built a real-time chat application using WebSockets and Node.js
+__RESUSEW_ITEM__ horizontal scaling,redis,docker
    \item Implemented horizontal scaling with Redis pub/sub and Docker
+__RESUSEW_ITEM__ postgresql,schema,persistence
    \item Designed a PostgreSQL schema for message persistence and search
+__RESUSEW_ITEM__ react,frontend,ui
    \item Created a React frontend with optimistic UI updates
+__RESUSEW_ITEM__ authentication
    \item Added authentication, presence tracking, and typing indicators
+__RESUSEW_ITEM__ deploy,kubernetes,ci,cd
    \item Deployed the system to Kubernetes with automated CI/CD
+__RESUSEW_END__ 3
\end{itemize}
```
now we have added some new lines to our project. each of these
new lines starts with a macro, such as `__RESUSEW_BEG__`.
together, these macros form a template, which resusew uses to
tailor your resume. lets take a look at what each of these
macros mean

### macros and templates

```
__RESUSEW_BEG__ real-time,websockets,node
```
the first macro we see is `__RESUSEW_BEG__`. this simply tells
resusew that this current line marks the beginning of a
template. there is some more text that follows, but dont worry
about that for now

```
__RESUSEW_ITEM__ react,frontend,ui
```
next lets look at `__RESUSEW_ITEM__`. each resusew template
contains several items, where an item is just a snippet of your
original resume content. for this example, each item is a
bullet point that describes our project. the `__RESUSEW_ITEM__`
macro marks the end of one item, and the start of a new one,
similar to a comma in a list

the remainder of the text we see is a comma-separated list of
keywords, for the item that follows. note that the first item
in our template doesnt have a `__RESUSEW_ITEM__` macro before
it, so instead we put our keywords with `__RESUSEW_BEG__`.
resusew scans the job description for each of these keywords,
and assigns a score to the item, based on how well they match

note: do **not** put `__RESUSEW_ITEM__` immediately following
`__RESUSEW_BEG__`

```
__RESUSEW_END__ 3
```
our final macro is `__RESUSEW_END__`, which simply marks the
end of the current template. the number that follows is how
many items we want resusew to select from the template. resusew
will calculate a score for each item based on its keywords, and
only keep the top scoring items, while omitting the rest. in
our example here, resusew will only keep the top 3 items

### nested templates

```diff
\hrule

\section{Projects}

+ __RESUSEW_BEG__
\textbf{Distributed Chat Platform}

Personal Project |
\href{linkToGithub}{\underline{GitHub}} |
\href{linkToWebsite}{\underline{Website}}

\begin{itemize}
__RESUSEW_BEG__ real-time,websockets,node
    \item Built a real-time chat application using WebSockets and Node.js
__RESUSEW_ITEM__ horizontal scaling,redis,docker
    \item Implemented horizontal scaling with Redis pub/sub and Docker
__RESUSEW_ITEM__ postgresql,schema,persistence
    \item Designed a PostgreSQL schema for message persistence and search
__RESUSEW_ITEM__ react,frontend,ui
    \item Created a React frontend with optimistic UI updates
__RESUSEW_ITEM__ authentication
    \item Added authentication, presence tracking, and typing indicators
__RESUSEW_ITEM__ deploy,kubernetes,ci,cd
    \item Deployed the system to Kubernetes with automated CI/CD
__RESUSEW_END__ 3
\end{itemize}

+ __RESUSEW_ITEM__ 
Mobile Fitness Tracker

Personal Project |
\href{linkToGithub}{\underline{GitHub}} |
\href{linkToWebsite}{\underline{Website}}

\begin{itemize}
__RESUSEW_BEG__ cross-platform,mobile,react native
    \item Developed a cross-platform mobile app using React Native
__RESUSEW_ITEM__ device sensors
    \item Integrated device sensors for step counting and activity tracking
__RESUSEW_ITEM__ backend,api,fastapi,postgresql
    \item Built a backend API using FastAPI and PostgreSQL
__RESUSEW_ITEM__ data synchronization
    \item Implemented offline-first data synchronization
__RESUSEW_ITEM__ analytics,data visualizations
    \item Added charts and analytics using custom data visualizations
__RESUSEW_ITEM__ ci pipelines
    \item Published test builds using automated mobile CI pipelines
__RESUSEW_END__ 3
\end{itemize}

+ __RESUSEW_ITEM__ 
Embedded IoT Sensor Network

Personal Project |
\href{linkToGithub}{\underline{GitHub}} |
\href{linkToWebsite}{\underline{Website}}

\begin{itemize}
__RESUSEW_BEG__ microcontrollers,c,c++,sensing
    \item Programmed microcontrollers in C and C++ for environmental sensing
__RESUSEW_ITEM__ communication,MQTT
    \item Implemented low-power communication over MQTT
__RESUSEW_ITEM__ gateway service,python,data aggregation
    \item Built a gateway service in Python for data aggregation
__RESUSEW_ITEM__ cloud,real-time,monitoring
    \item Designed a cloud dashboard for real-time monitoring
__RESUSEW_ITEM__ reliability,fault tolerance,ota
    \item Focused on reliability, fault tolerance, and OTA updates
__RESUSEW_END__ 3
\end{itemize}

+ __RESUSEW_ITEM__ 
3D Software Renderer

Personal Project |
\href{linkToGithub}{\underline{GitHub}} |

\begin{itemize}
__RESUSEW_BEG__ cpu,3d,render,c++
    \item Implemented a CPU-based 3D renderer from scratch in C++
__RESUSEW_ITEM__ math,vector,matrix
    \item Wrote a custom math library for vectors, matrices, and transforms
__RESUSEW_ITEM__ rasterization,shader
    \item Implemented triangle rasterization, depth buffering, and shading
__RESUSEW_ITEM__ lighting,texture
    \item Explored lighting models, transparency, and texture mapping
__RESUSEW_ITEM__ benchmark,optimize
    \item Benchmarked and optimized performance-critical code paths
__RESUSEW_END__ 3
\end{itemize}

+ __RESUSEW_ITEM__ 
Cloud-Based Log Aggregation System

Personal Project |
\href{linkToGithub}{\underline{GitHub}} |
\href{linkToWebsite}{\underline{Website}}

\begin{itemize}
__RESUSEW_BEG__ logging,architecture,udp,tcp
    \item Designed a centralized logging architecture using UDP and TCP
__RESUSEW_ITEM__ server,go
    \item Implemented a log ingestion server in Go
__RESUSEW_ITEM__ web,ui,search,filter
    \item Built a web UI for searching and filtering logs
__RESUSEW_ITEM__ logging,severity
    \item Added structured logging and severity levels
__RESUSEW_ITEM__ aws,autoscaling,monitoring
    \item Deployed on AWS with autoscaling and monitoring
__RESUSEW_END__ 3
\end{itemize}

+ __RESUSEW_ITEM__ 
Machine Learning Experiment Platform

Personal Project |
\href{linkToGithub}{\underline{GitHub}} |
\href{linkToWebsite}{\underline{Website}}

\begin{itemize}
__RESUSEW_BEG__ machine learning,python
    \item Built a platform for running ML experiments using Python
__RESUSEW_ITEM__ pytorch,tensorflow
    \item Integrated PyTorch and TensorFlow training pipelines
__RESUSEW_ITEM__ tracking,visualization
    \item Implemented experiment tracking and metric visualization
__RESUSEW_ITEM__ dataset,artifact
    \item Added dataset versioning and model artifact storage
__RESUSEW_ITEM__ reproducibility,automation
    \item Focused on reproducibility and automation
__RESUSEW_END__ 3
\end{itemize}

+ __RESUSEW_END__ 3

\hrule
```
any item in a template can also contain templates. this example
shows the rest of the projects section in our resume. we have a
top level template, where each item is one of our projects.
then, for each project, we have another template where each
item is a bullet for that project

note that in our top level template, there is no need to
repeat any keywords. keywords chosen by a template will be
forwarded to its parent item

### important tips

- for any template, try to keep all items roughly the same
size, otherwise you run the risk of your content overflowing to
a second page if larger items happen to be chosen
- try to assign keywords to items evenly. if you are more
thorough with one particular item, it could be more likely to
end up with a higher score, since more keywords means more
potential matches with the job description
- never include multiple keywords for the same thing. for
example, dont have multiple of `react`, `React`, or `react.js`.
if a job description does contain `react` or something similar,
you will end up with duplicate matches, and that item will have
a bias, similar to the previous point

## example workflow

once youre all done resusew-ifying your resume, youre ready to
start using it in your job search! heres an example workflow,
once again using LaTeX

let `resume.tex.resusew` be our resume template

let `jobdesc.txt` be our current job description

first find a job you wish to apply for. copy the job
description and paste it in `jobdesc.txt`

run resusew to resolve templates, and store the resulting latex
output in `resume.tex`
```
resusew resume.tex.resusew jobdesc.txt resume.tex
```

now compile our latex resume into a pdf. for this example we
are using the `tectonic` latex compiler
```
tectonic resume.tex
```

you should now have your tailored resume in pdf output in
`resume.pdf`. upload it to the job posting and apply!

for more convenience, combine everything into a script
```bash
#!/bin/bash

resusew resume.tex.resusew jobdesc.txt resume.tex
tectonic resume.tex
rm resume.tex
```

