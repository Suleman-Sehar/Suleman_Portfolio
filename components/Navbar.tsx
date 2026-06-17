"use client"
import { motion, useScroll, useTransform } from 'framer-motion'
import { person } from '@/lib/data'

const links = ['about','skills','projects','experience','contact']

export default function Navbar() {
  const { scrollY } = useScroll()
  const bg = useTransform(scrollY, [0, 80], ['rgba(10,10,15,0)', 'rgba(10,10,15,0.95)'])

  return (
    <motion.nav style={{ background: bg, backdropFilter: 'blur(12px)' }}
      className="fixed top-0 left-0 right-0 z-40 px-6 py-4 flex items-center justify-between"
    >
      <span className="font-display font-bold text-primary text-lg">
        {person.name.split(' ')[0]}<span style={{color:'#7C3AED'}}>.</span>
      </span>
      <div className="hidden md:flex gap-6">
        {links.map(l => (
          <a key={l} href={`#${l}`}
            className="text-muted hover:text-primary capitalize text-sm transition-colors">
            {l}
          </a>
        ))}
      </div>
    </motion.nav>
  )
}