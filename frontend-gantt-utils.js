export const PHASES = [
  { key: 'po',    label: 'PO Review',        color: '#3b82f6', weeks: 1, loeGroup: null  },
  { key: 'eng',   label: 'Engineering',       color: '#8b5cf6', weeks: 2, loeGroup: 'eng' },
  { key: 'mat',   label: 'Material Planning', color: '#06b6d4', weeks: 1, loeGroup: 'sc'  },
  { key: 'proc',  label: 'Procurement',       color: '#f59e0b', weeks: 4, loeGroup: 'sc'  },
  { key: 'prod',  label: 'Production',        color: '#ec4899', weeks: 4, loeGroup: 'prod'},
  { key: 'hol',   label: 'Holiday',           color: '#6b7280', weeks: 1, loeGroup: null  },
  { key: 'doc',   label: 'Documentation',     color: '#10b981', weeks: 1, loeGroup: null  },
  { key: 'float', label: 'Float',             color: '#f97316', weeks: 1, loeGroup: null  },
]

export const CATS = [
  { key: 'eng',  label: 'Engineering',    color: '#8b5cf6' },
  { key: 'sc',   label: 'Supply Chain',   color: '#06b6d4' },
  { key: 'prod', label: 'Production',     color: '#ec4899' },
  { key: 'pm',   label: 'Project Mgmt',   color: '#a78bfa' },
]

export const PM_PHASES = ['po', 'eng', 'mat', 'proc', 'prod', 'doc']
export const PM_COLOR  = '#a78bfa'
export const WEEK_W    = 52   // px per week column

export function getISOWeek(d) {
  const dt = new Date(d)
  dt.setHours(0, 0, 0, 0)
  dt.setDate(dt.getDate() + 3 - (dt.getDay() + 6) % 7)
  const w1 = new Date(dt.getFullYear(), 0, 4)
  return 1 + Math.round(((dt - w1) / 86400000 - 3 + (w1.getDay() + 6) % 7) / 7)
}

export function absW(year, week) { return year * 52 + week }
export function fromAbs(a) { const y = Math.floor((a - 1) / 52); return { year: y, week: a - y * 52 } }
export function fmt(v) { return v === 0 ? '0' : v % 1 === 0 ? String(v) : v.toFixed(1) }

export function buildSegments(proj) {
  let abs = absW(proj.year, proj.start_week)
  const scW = (proj.phases.mat || 0) + (proj.phases.proc || 0)
  return PHASES.map(ph => {
    const start = abs
    const dur = Math.max(0, proj.phases[ph.key] ?? ph.weeks)
    abs += dur
    const { year, week } = fromAbs(start)
    let loePerWeek = 0
    if (ph.loeGroup === 'eng'  && dur > 0) loePerWeek = (proj.loe?.eng  || 0) / dur
    if (ph.loeGroup === 'sc'   && scW > 0) loePerWeek = (proj.loe?.sc   || 0) / scW
    if (ph.loeGroup === 'prod' && dur > 0) loePerWeek = (proj.loe?.prod || 0) / dur
    return { key: ph.key, label: ph.label, color: ph.color, absStart: start, startYear: year, startWeek: week, dur, loeGroup: ph.loeGroup, loePerWeek }
  })
}

export function pmPerWeek(proj) {
  const segs = buildSegments(proj)
  const pmW = segs.filter(s => PM_PHASES.includes(s.key)).reduce((a, s) => a + s.dur, 0)
  return pmW > 0 ? (proj.loe?.pm || 0) / pmW : 0
}

export function computeWeeklyLoE(projects, weeks) {
  const map = {}
  weeks.forEach(wk => { map[wk.abs] = { eng: 0, sc: 0, prod: 0, pm: 0 } })
  projects.forEach(proj => {
    const segs = buildSegments(proj)
    const ppw  = pmPerWeek(proj)
    const pmSegs = segs.filter(s => PM_PHASES.includes(s.key))
    segs.forEach(seg => {
      if (seg.dur <= 0 || !seg.loeGroup) return
      for (let i = 0; i < seg.dur; i++) { const a = seg.absStart + i; if (map[a]) map[a][seg.loeGroup] += seg.loePerWeek }
    })
    if (ppw > 0) pmSegs.forEach(seg => {
      for (let i = 0; i < seg.dur; i++) { const a = seg.absStart + i; if (map[a]) map[a].pm += ppw }
    })
  })
  return map
}

export function buildWeeks(vsAbs, nw) {
  const todayAbs = absW(new Date().getFullYear(), getISOWeek(new Date()))
  return Array.from({ length: nw }, (_, i) => {
    const a = vsAbs + i
    const { year, week } = fromAbs(a)
    return { abs: a, week, year, isToday: a === todayAbs }
  })
}
