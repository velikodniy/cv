#import "@preview/fontawesome:0.5.0": *

#let primary-font = "Roboto"

#let colors = (
  primary: color.black,
  footer: color.gray
)

#let icons = (
  email: box(fa-icon("envelope", fill: colors.primary)),
  linkedin: box(fa-icon("linkedin", fill: colors.primary)),
  github: box(fa-icon("github", fill: colors.primary))
)

#let show-author(author) = {
  align(center)[
    #pad(bottom: 5pt)[
      #block[
        #set text(
          size: 28pt,
          style: "normal",
          font: primary-font,
        )
        #author
      ]
    ]
  ]
}

#let show-positions(positions, separator: sym.dot.c) = {
  set text(
    colors.primary,
    size: 10pt,
    weight: "regular",
  )
  let padding = box(width: 5pt)
  let padded-separator = text[#padding#separator#padding]
  align(center)[
    #smallcaps[#positions.join([#padded-separator])]
  ]
}

#let show-contacts(author, contacts) = {
  set box(height: 10pt)

  let separator = box(width: 5pt)

  align(center)[
    #set text(
      size: 10pt,
      weight: "regular",
      style: "normal",
    )
    #block[
      #align(horizon)[
        #if ("email" in contacts) [
          #icons.email
          #box[#link("mailto:" + contacts.email)[#contacts.email]]
        ]
        #if ("github" in contacts) [
          #separator
          #icons.github
          #box[#link("https://github.com/" + contacts.github)[#contacts.github]]
        ]
        #if ("linkedin" in contacts) [
          #separator
          #icons.linkedin
          #box[
            #link("https://www.linkedin.com/in/" + contacts.linkedin)[#author]
          ]
        ]
      ]
    ]
  ]
}

#let curriculum-vitae(
  author: none,
  contacts: (:),
  positions: (),
  body
) = {
  set document(
    author: author,
    title: author + "'s Curriculum Vitae",
  )

  set page(
    paper: "a4",
    margin: (left: 15mm, right: 15mm, top: 10mm, bottom: 10mm),
    footer: [
        #set align(right)
        #set text(size: 8pt, weight: "light", fill: colors.footer)
        Last Update: #datetime.today().display()
    ],
    footer-descent: 0pt,
  )

  set text(
    lang: "en",
    font: primary-font,
    size: 11pt,
    fill: colors.primary,
  )

  set par(
    spacing: 0.75em,
    justify: true,
  )

  show heading.where(level: 1): it => [
    #set text(
      size: 16pt,
      weight: "regular",
    )
    #set align(left)
    #set block(above: 1em)
    #text[#strong[#text(colors.primary)[#it.body.text]]]
    #box(width: 1fr, line(length: 100%))
  ]

  show heading.where(level: 2): it => {
    set text(
      colors.primary,
      size: 12pt,
      style: "normal",
      weight: "bold",
    )
    it.body
  }

  show heading.where(level: 3): it => {
    set text(
      size: 10pt,
      weight: "regular",
    )
    smallcaps[#it.body]
  }

  show-author(author)
  show-positions(positions)
  show-contacts(author, contacts)

  show link: it => [#underline(offset: 2pt)[#it]]

  body
}

#let show-both-sides(left, right) = {
  block[
    #left
    #box(width: 1fr)
    #right
  ]
}

#let job(
  company: "",
  position: none,
  location: "",
  date: "",
  body
) = {
  block(above: 1em, below: 0.65em)[
    #pad[
      #block[
        #set block(
          above: 0.7em,
          below: 0.7em,
        )
        #pad[
          #show-both-sides[
            == #position
          ][
            #text(size: 11pt, weight: "medium")[#location]
          ]
        ]
      ]
      #if company != "" or date != "" [
        #show-both-sides[
          === #company
        ][
          #text(weight: "light", size: 9pt)[#date]
        ]
      ]
    ]
  ]
  block[
    #set text(
      size: 10pt,
      style: "normal",
      weight: "light",
      fill: colors.primary,
    )
    #set par(leading: 0.65em)
    #block(above: 0.5em)[
      #body
    ]
  ]
}

#let skill(category, items) = {
  set block(below: 0.65em)
  set pad(top: 2pt)

  pad[
    #grid(
      columns: (20fr, 80fr),
      gutter: 10pt,
      align(right)[
        #set text(hyphenate: false)
        == #category
      ],
      align(left)[
        #set text(
          size: 11pt,
          style: "normal",
          weight: "light",
        )
        #items.join(", ")
      ],
    )
  ]
}
