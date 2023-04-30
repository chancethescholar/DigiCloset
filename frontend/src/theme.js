import { extendTheme } from '@chakra-ui/react'

const theme = extendTheme({
    colors: {
      transparent: 'transparent',
      black: '#000',
      white: '#fff',
      gray: {
        50: '#f7fafc',
        // ...
        900: '#171923',
      },
      red: {
        50: '#FFF5F5',
        300: '#FC8181',
        400: '#F56565',
        600: '#C53030',
        900: '#63171B',
      }
      // ...
    },
    fonts: {
      heading: `'Crafty Girls', sans-serif`,
      body: `'Cambay', sans-serif`,
    },
    sizes: {
      lg: '80rem'
    }
  })

  export default theme