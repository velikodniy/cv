#import "template.typ": *

#let data = yaml("data.yaml")

#show: curriculum-vitae.with(
  author: data.author,
  positions: data.positions,
  contacts: (
    email: data.contacts.email,
    github: data.contacts.github,
    linkedin: data.contacts.linkedin
  )
)

= Experience

#for exp in data.experience {
  let date = exp.startDate
  if "endDate" in exp {
    date += " --- " + exp.endDate
  }

  let highlights = ()
  if "highlights" in exp {
    highlights = exp.highlights.map(h => [- h])
  }

  job(
    position: exp.position,
    company: exp.company,
    location: exp.location,
    date: date,
  )[
    #if "highlights" in exp [
      #for h in exp.highlights [
        - #h
      ]
    ]
  ]
}

= Education

#for edu in data.education [
  #let date = edu.startDate
  #if "endDate" in edu [
    #date += " --- " + edu.endDate
  ]

  #job(
    position: edu.degree,
    company: edu.institution,
    date: date,
  )[
    #if "details" in edu [
      #for detail in edu.details [
        - #detail
      ]
    ]
    #if "gpa" in edu [
      - GPA: #edu.gpa
    ]
  ]
]

= Skills

#for (skill_category, skills_list) in data.skills.pairs() {
  let details = skills_list.map(d => d.name + " (" + d.level + ")")
  skill(skill_category, details)
}
