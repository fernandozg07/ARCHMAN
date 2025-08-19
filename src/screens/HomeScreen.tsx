import React from 'react';
import { View, Text, StyleSheet, ScrollView, TouchableOpacity } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { useAppStore } from '../store/AppStore';
import { theme } from '../styles/theme';

export default function HomeScreen({ navigation }: any) {
  const { user } = useAppStore();
  const userColor = user?.user_type ? theme.colors[user.user_type] : theme.colors.primary;

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView showsVerticalScrollIndicator={false}>
        <View style={styles.header}>
          <View>
            <Text style={styles.welcomeText}>⚡ ARCHMAN</Text>
            <Text style={styles.subtitle}>Olá, {user?.first_name || 'Usuário'}</Text>
            <Text style={[styles.userType, { color: userColor }]}>
              {user?.user_type === 'admin' ? 'Administrador' : 
               user?.user_type === 'officer' ? 'Officer' : 'Usuário'}
            </Text>
          </View>
          <View style={[styles.headerIcon, { backgroundColor: userColor + '20' }]}>
            <Ionicons name="flash" size={32} color={userColor} />
          </View>
        </View>

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Ações Rápidas</Text>
          
          <TouchableOpacity 
            style={styles.actionButton}
            onPress={() => navigation.navigate('Camera' as never)}
          >
            <View style={styles.actionIcon}>
              <Ionicons name="camera" size={28} color="white" />
            </View>
            <View style={styles.actionContent}>
              <Text style={styles.actionTitle}>Fotografar Conta</Text>
              <Text style={styles.actionSubtitle}>Escaneie sua conta de energia</Text>
            </View>
            <Ionicons name="chevron-forward" size={20} color="white" />
          </TouchableOpacity>
          
          <TouchableOpacity 
            style={[styles.actionButton, { backgroundColor: '#2196F3' }]}
            onPress={() => navigation.navigate('Dashboard' as never)}
          >
            <View style={styles.actionIcon}>
              <Ionicons name="analytics" size={28} color="white" />
            </View>
            <View style={styles.actionContent}>
              <Text style={styles.actionTitle}>Dashboard</Text>
              <Text style={styles.actionSubtitle}>Veja seus gráficos e dados</Text>
            </View>
            <Ionicons name="chevron-forward" size={20} color="white" />
          </TouchableOpacity>
          
          {user?.user_type === 'admin' && (
            <TouchableOpacity 
              style={[styles.actionButton, { backgroundColor: theme.colors.admin }]}
              onPress={() => navigation.navigate('AdminDashboard' as never)}
            >
              <View style={styles.actionIcon}>
                <Ionicons name="settings" size={28} color="white" />
              </View>
              <View style={styles.actionContent}>
                <Text style={styles.actionTitle}>Painel Admin</Text>
                <Text style={styles.actionSubtitle}>Gerenciar sistema</Text>
              </View>
              <Ionicons name="chevron-forward" size={20} color="white" />
            </TouchableOpacity>
          )}
          
          {user?.user_type === 'officer' && (
            <TouchableOpacity 
              style={[styles.actionButton, { backgroundColor: theme.colors.officer }]}
              onPress={() => navigation.navigate('Financial' as never)}
            >
              <View style={styles.actionIcon}>
                <Ionicons name="wallet" size={28} color="white" />
              </View>
              <View style={styles.actionContent}>
                <Text style={styles.actionTitle}>Painel Financeiro</Text>
                <Text style={styles.actionSubtitle}>Gerenciar clientes</Text>
              </View>
              <Ionicons name="chevron-forward" size={20} color="white" />
            </TouchableOpacity>
          )}
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: theme.colors.background,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: theme.spacing.lg,
    backgroundColor: theme.colors.surface,
    marginBottom: theme.spacing.lg,
  },
  welcomeText: {
    fontSize: 24,
    fontWeight: 'bold',
    color: theme.colors.primary,
    marginBottom: 4,
  },
  subtitle: {
    fontSize: 16,
    color: theme.colors.text,
    marginBottom: 2,
  },
  userType: {
    fontSize: 12,
    fontWeight: '600',
    textTransform: 'uppercase',
  },
  headerIcon: {
    width: 60,
    height: 60,
    borderRadius: 30,
    justifyContent: 'center',
    alignItems: 'center',
  },
  section: {
    padding: theme.spacing.lg,
  },
  sectionTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: theme.colors.text,
    marginBottom: theme.spacing.md,
  },
  actionButton: {
    backgroundColor: theme.colors.primary,
    flexDirection: 'row',
    alignItems: 'center',
    padding: theme.spacing.lg,
    borderRadius: theme.borderRadius.lg,
    marginBottom: theme.spacing.md,
    shadowColor: theme.colors.primary,
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 12,
    elevation: 8,
  },
  actionIcon: {
    width: 50,
    height: 50,
    borderRadius: 25,
    backgroundColor: 'rgba(255,255,255,0.2)',
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 16,
  },
  actionContent: {
    flex: 1,
  },
  actionTitle: {
    color: 'white',
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 4,
  },
  actionSubtitle: {
    color: 'rgba(255,255,255,0.8)',
    fontSize: 14,
  },
});