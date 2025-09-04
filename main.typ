#import "resume.typ": *

#let data = yaml("data.yaml")

#let render-markdown-links(text) = {
  let link_regex = regex("\[([^\]]+)\]\(([^)]+)\)")
  show link_regex: it => {
    let m = it.text.match(link_regex)
    let link_text = m.captures.at(0)
    let url = m.captures.at(1)
    link(url)[#link_text]
  }
  text
}

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
  job(
    position: exp.position,
    company: exp.company,
    location: exp.location,
    date: date-range(exp.dates),
  )[
    #if "highlights" in exp [
      #for h in exp.highlights [
        - #render-markdown-links(h)
      ]
    ]
  ]
}

= Education

#for edu in data.education [
  #job(
    position: edu.degree,
    company: edu.institution,
    date: date-range(edu.dates),
  )[
    #if "details" in edu [
      #for detail in edu.details [
        - #render-markdown-links(detail)
      ]
    ]
    #if "gpa" in edu [
      - GPA: #edu.gpa
    ]
  ]
]

= Patents

#for patent in data.patents [
  - #patent.title (#link(patent.link)[#patent.code])
]

= Skills

#for (skill_category, skills_list) in data.skills.pairs() {
  let details = skills_list.map(d => d.name + " (" + d.level + ")")
  skill(skill_category, details)
}
