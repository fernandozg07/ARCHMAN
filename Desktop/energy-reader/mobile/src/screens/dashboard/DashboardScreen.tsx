import React, { useEffect, useState } from 'react';
import { View, StyleSheet, ScrollView, RefreshControl } from 'react-native';
import { Card, Text, Button, ActivityIndicator } from 'react-native-paper';
import { useQuery } from '@tanstack/react-query';
import { api } from '../../services/api';
import { useAuthStore } from '../../store/authStore';

export default function DashboardScreen({ navigation }: any) {
  const { user } = useAuthStore();
  const [refreshing, setRefreshing] = useState(false);

  const { data: bills, isLoading, refetch } = useQuery({
    queryKey: ['bills'],
    queryFn: () => api.getBills(),
  });

  const { data: analytics } = useQuery({
    queryKey: ['analytics'],
    queryFn: () => api.getAnalyticsSummary(),
  });

  const onRefresh = async () => {
    setRefreshing(true);
    await refetch();
    setRefreshing(false);
  };

  if (isLoading) {
    return (
      <View style={styles.loading}>
        <ActivityIndicator size="large" />
        <Text>Carregando dados...</Text>
      </View>
    );
  }

  return (
    <ScrollView
      style={styles.container}
      refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh} />}
    >
      <Card style={styles.welcomeCard}>
        <Card.Content>
          <Text variant="headlineSmall">
            Olá, {user?.first_name || 'Usuário'}! 👋
          </Text>
          <Text variant="bodyMedium" style={styles.subtitle}>
            Bem-vindo ao Energy Reader
          </Text>
        </Card.Content>
      </Card>

      <View style={styles.statsContainer}>
        <Card style={styles.statCard}>
          <Card.Content>
            <Text variant="headlineMedium" style={styles.statNumber}>
              {bills?.results?.length || 0}
            </Text>
            <Text variant="bodySmall">Contas Enviadas</Text>
          </Card.Content>
        </Card>

        <Card style={styles.statCard}>
          <Card.Content>
            <Text variant="headlineMedium" style={styles.statNumber}>
              R$ {analytics?.total_value || '0,00'}
            </Text>
            <Text variant="bodySmall">Valor Total</Text>
          </Card.Content>
        </Card>
      </View>

      <Card style={styles.actionCard}>
        <Card.Content>
          <Text variant="titleMedium" style={styles.actionTitle}>
            Ações Rápidas
          </Text>
          <Button
            mode="contained"
            icon="camera"
            style={styles.actionButton}
            onPress={() => navigation.navigate('Upload')}
          >
            Enviar Nova Conta
          </Button>
          <Button
            mode="outlined"
            icon="chart-line"
            style={styles.actionButton}
            onPress={() => navigation.navigate('History')}
          >
            Ver Histórico
          </Button>
        </Card.Content>
      </Card>

      <Card style={styles.recentCard}>
        <Card.Content>
          <Text variant="titleMedium" style={styles.sectionTitle}>
            Contas Recentes
          </Text>
          {bills?.results?.slice(0, 3).map((bill: any, index: number) => (
            <View key={index} style={styles.billItem}>
              <View>
                <Text variant="bodyMedium">{bill.fornecedor || 'Processando...'}</Text>
                <Text variant="bodySmall" style={styles.billDate}>
                  {new Date(bill.created_at).toLocaleDateString('pt-BR')}
                </Text>
                <Text variant="bodySmall" style={{
                  color: bill.status === 'PROCESSED' ? '#4CAF50' : 
                         bill.status === 'PROCESSING' ? '#FF9800' : '#F44336'
                }}>
                  {bill.status === 'PROCESSED' ? 'Processado' :
                   bill.status === 'PROCESSING' ? 'Processando' :
                   bill.status === 'FAILED' ? 'Erro' : 'Enviado'}
                </Text>
              </View>
              <View style={{ alignItems: 'flex-end' }}>
                <Text variant="bodyMedium" style={styles.billValue}>
                  {bill.valor_total ? `R$ ${parseFloat(bill.valor_total).toFixed(2)}` : 'Processando...'}
                </Text>
                {bill.consumo_kwh && (
                  <Text variant="bodySmall" style={styles.billConsumption}>
                    {bill.consumo_kwh} kWh
                  </Text>
                )}
              </View>
            </View>
          ))}
          {(!bills?.results || bills.results.length === 0) && (
            <Text style={styles.emptyText}>
              Nenhuma conta encontrada. Envie sua primeira conta!
            </Text>
          )}
        </Card.Content>
      </Card>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
    padding: 15,
  },
  loading: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  welcomeCard: {
    marginBottom: 15,
  },
  subtitle: {
    color: '#666',
    marginTop: 5,
  },
  statsContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 15,
  },
  statCard: {
    flex: 1,
    marginHorizontal: 5,
  },
  statNumber: {
    color: '#2E7D32',
    fontWeight: 'bold',
  },
  actionCard: {
    marginBottom: 15,
  },
  actionTitle: {
    marginBottom: 15,
  },
  actionButton: {
    marginBottom: 10,
  },
  recentCard: {
    marginBottom: 15,
  },
  sectionTitle: {
    marginBottom: 15,
  },
  billItem: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: 10,
    borderBottomWidth: 1,
    borderBottomColor: '#eee',
  },
  billDate: {
    color: '#666',
    marginTop: 2,
  },
  billValue: {
    fontWeight: 'bold',
    color: '#2E7D32',
  },
  billConsumption: {
    color: '#666',
    fontSize: 12,
  },
  emptyText: {
    textAlign: 'center',
    color: '#666',
    fontStyle: 'italic',
    paddingVertical: 20,
  },
});