
language: PYTHON
name:     "spearmintRunner"

variable {
 name: "FIGHT_MODE"
 type: ENUM
 size: 2
 options: "on"
 options: "off"
}

variable {
  name: "EXPLORING"
  type: ENUM
  size: 2
  options: "random"
  options: "heuristic"
}

variable {
  name: "SOURCES"
  type: ENUM
  size: 3
  options: "walktroughs"
  options: "tutorials"
  options: "all"
}
