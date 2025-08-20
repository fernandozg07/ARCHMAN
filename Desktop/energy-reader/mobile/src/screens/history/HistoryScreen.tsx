import React from 'react';
import { View, StyleSheet, FlatList, RefreshControl } from 'react-native';
import { Card, Text, Chip, ActivityIndicator } from 'react-native-paper';
import { useQuery } from '@tanstack/react-query';
import { api } from '../../services/api';

export default function HistoryScreen({ navigation }: any) {
  const { data: bills, isLoading, refetch } = useQuery({
    queryKey: ['bills'],
    queryFn: () => api.getBills(),
  });

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'PROCESSED': return '#4CAF50';
      case 'PROCESSING': return '#FF9800';
      case 'FAILED': return '#F44336';
      default: return '#9E9E9E';
    }
  };

  const getStatusText = (status: string) => {
    switch (status) {
      case 'PROCESSED': return 'Processado';
      case 'PROCESSING': return 'Processando';
      case 'FAILED': return 'Erro';
      case 'UPLOADED': return 'Enviado';
      default: return status;
    }
  };

  const renderBill = ({ item }: { item: any }) => (
    <Card style={styles.billCard} onPress={() => navigation.navigate('BillDetail', { bill: item })}>
      <Card.Content>
        <View style={styles.billHeader}>
          <Text variant="titleMedium">{item.fornecedor || 'Fornecedor'}</Text>
          <Chip 
            mode="flat" 
            textStyle={{ color: getStatusColor(item.status) }}
            style={{ backgroundColor: `${getStatusColor(item.status)}20` }}
          >
            {getStatusText(item.status)}
          </Chip>
        </View>

        <View style={styles.billDetails}>
          <View style={styles.detailRow}>
            <Text variant="bodySmall" style={styles.label}>Cliente:</Text>
            <Text variant="bodyMedium">{item.numero_cliente || 'N/A'}</Text>
          </View>

          {item.consumo_kwh && (
            <View style={styles.detailRow}>
              <Text variant="bodySmall" style={styles.label}>Consumo:</Text>
              <Text variant="bodyMedium">{item.consumo_kwh} kWh</Text>
            </View>
          )}

          {item.valor_total && (
            <View style={styles.detailRow}>
              <Text variant="bodySmall" style={styles.label}>Valor:</Text>
              <Text variant="bodyMedium" style={styles.value}>
                R$ {parseFloat(item.valor_total).toFixed(2)}
              </Text>
            </View>
          )}

          <View style={styles.detailRow}>
            <Text variant="bodySmall" style={styles.label}>Enviado em:</Text>
            <Text variant="bodySmall">
              {new Date(item.created_at).toLocaleDateString('pt-BR')}
            </Text>
          </View>
        </View>
      </Card.Content>
    </Card>
  );

  if (isLoading) {
    return (
      <View style={styles.loading}>
        <ActivityIndicator size="large" />
        <Text>Carregando histórico...</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <FlatList
        data={bills?.results || []}
        renderItem={renderBill}
        keyExtractor={(item) => item.id.toString()}
        refreshControl={
          <RefreshControl refreshing={isLoading} onRefresh={refetch} />
        }
        ListEmptyComponent={
          <View style={styles.empty}>
            <Text variant="bodyLarge" style={styles.emptyText}>
              Nenhuma conta encontrada
            </Text>
            <Text variant="bodyMedium" style={styles.emptySubtext}>
              Envie sua primeira conta para ver o histórico aqui
            </Text>
          </View>
        }
        contentContainerStyle={styles.listContainer}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  loading: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  listContainer: {
    padding: 15,
  },
  billCard: {
    marginBottom: 15,
  },
  billHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 15,
  },
  billDetails: {
    gap: 8,
  },
  detailRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  label: {
    color: '#666',
    fontWeight: '500',
  },
  value: {
    fontWeight: 'bold',
    color: '#2E7D32',
  },
  empty: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    paddingTop: 100,
  },
  emptyText: {
    textAlign: 'center',
    marginBottom: 10,
    color: '#666',
  },
  emptySubtext: {
    textAlign: 'center',
    color: '#999',
  },
});