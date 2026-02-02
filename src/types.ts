export interface Contact {
  email: string;
  github: string;
  linkedin: string;
}

export interface JobDate {
  start: string;
  end?: string;
}

export interface Job {
  position: string;
  company: string;
  location: string;
  dates: JobDate;
  highlights: string[];
  techStack?: string[];
}

export interface GPA {
  value: number | string;
  max: number | string;
}

export interface Education {
  institution: string;
  major: string;
  degree: string;
  honor?: boolean;
  graduated?: boolean;
  dates: JobDate;
  gpa?: GPA;
  highlights: string[];
}

export interface Language {
  name: string;
  level: string;
}

export interface Skills {
  languages: Language[];
}

export interface Patent {
  code: string;
  title: string;
  link: string;
}

export interface ResumeData {
  author: string;
  base_url: string;
  photo: string;
  pdf_filename: string;
  about: string;
  positions: string[];
  location: string;
  contacts: Contact;
  experience: Job[];
  education: Education[];
  skills: Skills;
  patents: Patent[];
}
