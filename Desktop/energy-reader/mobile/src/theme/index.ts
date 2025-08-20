import { MD3LightTheme, MD3DarkTheme } from 'react-native-paper';

const lightColors = {
  primary: '#2E7D32',
  primaryContainer: '#A5D6A7',
  secondary: '#4CAF50',
  secondaryContainer: '#C8E6C9',
  tertiary: '#FF9800',
  tertiaryContainer: '#FFE0B2',
  surface: '#FFFFFF',
  surfaceVariant: '#F5F5F5',
  background: '#FAFAFA',
  error: '#D32F2F',
  errorContainer: '#FFCDD2',
  onPrimary: '#FFFFFF',
  onPrimaryContainer: '#1B5E20',
  onSecondary: '#FFFFFF',
  onSecondaryContainer: '#2E7D32',
  onTertiary: '#FFFFFF',
  onTertiaryContainer: '#E65100',
  onSurface: '#212121',
  onSurfaceVariant: '#424242',
  onBackground: '#212121',
  onError: '#FFFFFF',
  onErrorContainer: '#B71C1C',
  outline: '#BDBDBD',
  outlineVariant: '#E0E0E0',
  shadow: '#000000',
  scrim: '#000000',
  inverseSurface: '#303030',
  inverseOnSurface: '#F5F5F5',
  inversePrimary: '#81C784',
};

const darkColors = {
  primary: '#81C784',
  primaryContainer: '#2E7D32',
  secondary: '#A5D6A7',
  secondaryContainer: '#388E3C',
  tertiary: '#FFB74D',
  tertiaryContainer: '#F57C00',
  surface: '#121212',
  surfaceVariant: '#1E1E1E',
  background: '#000000',
  error: '#EF5350',
  errorContainer: '#C62828',
  onPrimary: '#1B5E20',
  onPrimaryContainer: '#C8E6C9',
  onSecondary: '#2E7D32',
  onSecondaryContainer: '#E8F5E8',
  onTertiary: '#E65100',
  onTertiaryContainer: '#FFF3E0',
  onSurface: '#FFFFFF',
  onSurfaceVariant: '#E0E0E0',
  onBackground: '#FFFFFF',
  onError: '#FFFFFF',
  onErrorContainer: '#FFEBEE',
  outline: '#757575',
  outlineVariant: '#424242',
  shadow: '#000000',
  scrim: '#000000',
  inverseSurface: '#F5F5F5',
  inverseOnSurface: '#303030',
  inversePrimary: '#2E7D32',
};

export const lightTheme = {
  ...MD3LightTheme,
  colors: {
    ...MD3LightTheme.colors,
    ...lightColors,
  },
};

export const darkTheme = {
  ...MD3DarkTheme,
  colors: {
    ...MD3DarkTheme.colors,
    ...darkColors,
  },
};

// Theme provider function for dynamic switching
export const getTheme = (isDark: boolean = false) => isDark ? darkTheme : lightTheme;

// Default export
export default lightTheme;