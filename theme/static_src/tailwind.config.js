/**
 * This is a minimal config.
 *
 * If you need the full config, get it from here:
 * https://unpkg.com/browse/tailwindcss@latest/stubs/defaultConfig.stub.js
 */

module.exports = {
  content: [
    /**
     * HTML. Paths to Django template files that will contain Tailwind CSS classes.
     */

    /*  Templates within theme app (<tailwind_app_name>/templates), e.g. base.html. */
    '../templates/**/*.html',

    /*
     * Main templates directory of the project (BASE_DIR/templates).
     * Adjust the following line to match your project structure.
     */
    '../../templates/**/*.html',

    /*
     * Templates in other django apps (BASE_DIR/<any_app_name>/templates).
     * Adjust the following line to match your project structure.
     */
    '../../**/templates/**/*.html',

    /**
     * JS: If you use Tailwind CSS in JavaScript, uncomment the following lines and make sure
     * patterns match your project structure.
     */
    /* JS 1: Ignore any JavaScript in node_modules folder. */
    // '!../../**/node_modules',
    /* JS 2: Process all JavaScript files in the project. */
    // '../../**/*.js',

    /**
     * Python: If you use Tailwind CSS classes in Python, uncomment the following line
     * and make sure the pattern below matches your project structure.
     */
    // '../../**/*.py'
  ],
  theme: {
    extend: {
      colors: {
        base: {
          bg: '#EFF3FF',
          depth: '#E3E8F8',
          pressure: '#D7DDF4',
          field: '#272D3D',
          sub: '#788196',
          smoke: '#F0F0F0',
        },
        slate: {
          50: '#f8fafc',
          100: '#dee2e6',
          200: '#cbd3da',
          300: '#a8b8d8',
          400: '#8392ab',
          500: '#67748e',
          600: '#627594',
          700: '#344767',
          800: '#3a416f',
          900: '#051139',
          container: '#D9E0F2',
        },
        gray: {
          50: '#f8f9fa',
          100: '#ebeff4',
          200: '#e9ecef',
          300: '#d2d6da',
          400: '#ced4da',
          500: '#adb5bd',
          600: '#6c757d',
          700: '#495057',
          800: '#252f40',
          900: '#141727',
        },
        zinc: {
          50: '#fafafa',
          100: '#f4f4f5',
          200: '#e4e4e7',
          300: '#d4d4d8',
          400: '#a1a1aa',
          500: '#71717a',
          600: '#52525b',
          700: '#212529',
          800: '#212229',
          900: '#18181b',
        },
        neutral: {
          50: '#fafafa',
          100: '#f5f5f5',
          200: '#e5e5e5',
          300: '#d4d4d4',
          400: '#a3a3a3',
          500: '#737373',
          600: '#525252',
          700: '#404040',
          800: '#262626',
          900: '#111111',
        },
        stone: {
          50: '#fafaf9',
          100: '#f5f5f4',
          200: '#e7e5e4',
          300: '#d6d3d1',
          400: '#a8a29e',
          500: '#78716c',
          600: '#57534e',
          700: '#44403c',
          800: '#292524',
          900: '#1c1917',
        },
        red: {
          50: '#fef2f2',
          100: '#fee2e2',
          200: '#fecaca',
          300: '#fca5a5',
          400: '#f87171',
          500: '#f53939',
          600: '#f5365c',
          700: '#b91c1c',
          800: '#991b1b',
          900: '#7f1d1d',
        },
        orange: {
          50: '#fff7ed',
          100: '#ffedd5',
          200: '#fed7aa',
          300: '#fdba74',
          400: '#fb923c',
          500: '#fb6340',
          600: '#f56036',
          700: '#c2410c',
          800: '#9a3412',
          900: '#7c2d12',
        },
        amber: {
          50: '#fffbeb',
          100: '#fef3c7',
          200: '#fde68a',
          300: '#fcd34d',
          400: '#fbbf24',
          500: '#f59e0b',
          600: '#d97706',
          700: '#b45309',
          800: '#92400e',
          900: '#78350f',
        },
        yellow: {
          50: '#fefce8',
          100: '#fef9c3',
          200: '#fef08a',
          300: '#fde047',
          400: '#fbcf33',
          500: '#fbb140',
          600: '#ca8a04',
          700: '#a16207',
          800: '#854d0e',
          900: '#713f12',
        },
        lime: {
          50: '#f7fee7',
          100: '#ecfccb',
          200: '#d9f99d',
          300: '#bef264',
          400: '#98ec2d',
          500: '#82d616',
          600: '#65a30d',
          700: '#4d7c0f',
          800: '#3f6212',
          900: '#365314',
        },
        green: {
          50: '#f0fdf4',
          100: '#dcfce7',
          200: '#bbf7d0',
          300: '#86efac',
          400: '#4ade80',
          500: '#22c55e',
          600: '#17ad37',
          700: '#15803d',
          800: '#166534',
          900: '#14532d',
        },
        emerald: {
          50: '#ecfdf5',
          100: '#d1fae5',
          200: '#a7f3d0',
          300: '#6ee7b7',
          400: '#34d399',
          500: '#2dce89',
          600: '#059669',
          700: '#047857',
          800: '#065f46',
          900: '#064e3b',
        },
        teal: {
          50: '#f0fdfa',
          100: '#ccfbf1',
          200: '#99f6e4',
          300: '#5eead4',
          400: '#2dcecc',
          500: '#14b8a6',
          600: '#0d9488',
          700: '#0f766e',
          800: '#115e59',
          900: '#134e4a',
        },
        cyan: {
          50: '#ecfeff',
          100: '#cffafe',
          200: '#a5f3fc',
          300: '#67e8f9',
          400: '#21d4fd',
          500: '#11cdef',
          600: '#0891b2',
          700: '#0e7490',
          800: '#155e75',
          900: '#164e63',
        },
        sky: {
          50: '#f0f9ff',
          100: '#f6f9fc',
          200: '#bae6fd',
          300: '#7dd3fc',
          400: '#38bdf8',
          500: '#0ea5e9',
          600: '#3ea1ec',
          700: '#0369a1',
          800: '#075985',
          900: '#0e456d',
        },
        blue: {
          50: '#eff6ff',
          100: '#dbeafe',
          200: '#bfdbfe',
          300: '#93c5fd',
          400: '#60a5fa',
          500: '#5e72e4',
          600: '#2152ff',
          700: '#1171ef',
          800: '#344e86',
          900: '#00007d',
        },
        indigo: {
          50: '#eef2ff',
          100: '#e0e7ff',
          200: '#c7d2fe',
          300: '#a5b4fc',
          400: '#818cf8',
          500: '#6366f1',
          600: '#4f46e5',
          700: '#4338ca',
          800: '#3730a3',
          900: '#312e81',
        },
        violet: {
          50: '#f5f3ff',
          100: '#ede9fe',
          200: '#ddd6fe',
          300: '#c4b5fd',
          400: '#a78bfa',
          500: '#825ee4',
          600: '#7c3aed',
          700: '#6d28d9',
          800: '#5b21b6',
          900: '#4c1d95',
        },
        purple: {
          50: '#faf5ff',
          100: '#f3e8ff',
          200: '#e9d5ff',
          300: '#d8b4fe',
          400: '#c084fc',
          500: '#a855f7',
          600: '#9333ea',
          700: '#7928ca',
          800: '#6b21a8',
          900: '#581c87',
        },
        fuchsia: {
          50: '#fdf4ff',
          100: '#fae8ff',
          200: '#f5d0fe',
          300: '#e293d3',
          400: '#e879f9',
          500: '#cb0c9f',
          600: '#c026d3',
          700: '#a21caf',
          800: '#830866',
          900: '#701a75',
        },
        pink: {
          50: '#fdf2f8',
          100: '#fce7f3',
          200: '#fbcfe8',
          300: '#f9a8d4',
          400: '#f472b6',
          500: '#ff0080',
          600: '#db2777',
          700: '#be185d',
          800: '#9d174d',
          900: '#831843',
        },
        rose: {
          50: '#fff1f2',
          100: '#ffe4e6',
          200: '#fecdd3',
          300: '#fda4af',
          400: '#ff667c',
          500: '#f43f5e',
          600: '#e11d48',
          700: '#be123c',
          800: '#9f1239',
          900: '#881337',
        },
      },
      fontFamily: {
        notoSans: ['"Noto Sans"', 'Poppins', '"Sans Serif"'],
        dmSans: ['"DM Sans"', 'Poppins', 'Inter', '"Sans Serif"'],
        jost: ['Jost', 'Inter', '"Klee One"', '"Sans Serif"'],
        openSans: ['"Open Sans"', 'Caveat', '"DM Sans"', '"Noto Sans"', '"Sans Serif"'],
        montserrat: ['Montserrat', '"Open Sans"', '"Sans Serif"'],
        mulish: ['Mulish', '"Sans Serif"'],
        poppins: ['Poppins', 'Mulish', '"Sans Serif"'],
        quicksand: ['Quicksand', 'Mulish', 'Poppins', '"Sans Serif"'],
        kleeOne: ['"Klee One"', 'Poppins', 'cursive', '"Sans Serif"'],
        kaiseiDecol: ['"Kaisei Decol"', '"Klee One"', 'Quicksand', 'Serif'],
        dancingScript: ['"Dancing Script"', 'Mulish', 'cursive'],
        inter: ['Inter', 'Poppins', 'Mulish', '"Sans Serif"'],
        caveat: ['Caveat', '"Klee One"', 'Poppins', 'Inter', 'Cursive'],
      },
      boxShadow: {
        container1: '0px 14px 19px -8px #00000005, 0px 14px 34px -20px #0000000f',
        container2:
          '0 12px 22px -5px rgb(0 0 0 / 4%), 0 10px 10px -5px rgb(0 0 0 / 3%), 1px 8px 24px 2px rgb(0 0 0 / 2%)',
        container3:
          '0 12px 24px -5px rgb(0 0 0 / 3%), 0 11px 14px -6px rgb(0 0 0 / 2%), 0px 11px 27px -2px rgb(0 0 0 / 1%)',
        priceWidget: '0 10px 17px -12px rgb(58 65 111), 0 16px 27px -16px rgb(58 65 111 / 38%)',
      },
    },
  },
  plugins: [
    /**
     * '@tailwindcss/forms' is the forms plugin that provides a minimal styling
     * for forms. If you don't like it or have own styling for forms,
     * comment the line below to disable '@tailwindcss/forms'.
     */
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
    require('@tailwindcss/line-clamp'),
    require('@tailwindcss/aspect-ratio'),
  ],
};
