/**
 * Tailwind CSS Default Purple Color Scale
 * Exact hex values from Tailwind CSS v3 defaults
 * Used to match the original template design precisely
 */

export const tailwindPurpleTheme = {
  name: 'Tailwind Purple (Original)',
  description: 'Exact Tailwind CSS default purple colors - matches original templates',
  
  // Tailwind Purple - Light Mode
  light: [
    '#fafafb',  // Step 1 (custom - slightly darker than white for backgrounds)
    '#faf5ff',  // Step 2 (Tailwind purple-50)
    '#f3e8ff',  // Step 3 (Tailwind purple-100)
    '#e9d5ff',  // Step 4 (Tailwind purple-200)
    '#d8b4fe',  // Step 5 (Tailwind purple-300)
    '#c084fc',  // Step 6 (Tailwind purple-400)
    '#a855f7',  // Step 7 (Tailwind purple-500)
    '#9333ea',  // Step 8 (Tailwind purple-600) - PRIMARY
    '#7e22ce',  // Step 9 (Tailwind purple-700)
    '#6b21a8',  // Step 10 (Tailwind purple-800)
    '#581c87',  // Step 11 (Tailwind purple-900) - Accessible text
    '#3b0764'   // Step 12 (Tailwind purple-950) - High contrast text
  ],
  
  // Tailwind Purple - Dark Mode
  dark: [
    '#18111c',  // Step 1 (darkest background)
    '#231825',  // Step 2 (dark background)
    '#3b0764',  // Step 3 (Tailwind purple-950)
    '#581c87',  // Step 4 (Tailwind purple-900)
    '#6b21a8',  // Step 5 (Tailwind purple-800)
    '#7e22ce',  // Step 6 (Tailwind purple-700)
    '#9333ea',  // Step 7 (Tailwind purple-600) - PRIMARY
    '#a855f7',  // Step 8 (Tailwind purple-500)
    '#c084fc',  // Step 9 (Tailwind purple-400) - Interactive elements
    '#d8b4fe',  // Step 10 (Tailwind purple-300)
    '#e9d5ff',  // Step 11 (Tailwind purple-200) - Accessible text
    '#f3e8ff'   // Step 12 (Tailwind purple-100) - High contrast text
  ]
};

