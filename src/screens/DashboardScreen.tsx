import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet, ScrollView, Dimensions } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { useAppStore } from '../store/AppStore';
import { apiService } from '../services/api';
import { theme } from '../styles/theme';

const { width } = Dimensions.get('window');

export default function DashboardScreen() {
  const { bills, user } = useAppStore();
  const [analytics, setAnalytics] = useState<any>(null);
  
  const userColor = user?.user_type === 'admin' ? '#e91e63' : 
                   user?.user_type === 'officer' ? '#9c27b0' : '#00d4aa';

  useEffect(() => {
    loadAnalytics();
  }, [bills]);

  const loadAnalytics = async () => {
    try {
      const data = await apiService.getAnalytics();
      setAnalytics(data);
    } catch (error) {
      console.error('Error loading analytics:', error);
    }
  };

  const recentBills = bills.slice(0, 3);
  const lastBill = bills[0];
  const previousBill = bills[1];
  
  const changePercent = lastBill && previousBill 
    ? ((lastBill.consumo_kwh - previousBill.consumo_kwh) / previousBill.consumo_kwh * 100).toFixed(1)
    : '0';

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView showsVerticalScrollIndicator={false}>
        {/* KPIs */}
        <View style={styles.kpiContainer}>
          <View style={styles.kpiCard}>
            <Ionicons name="flash" size={24} color={userColor} />
            <Text style={styles.kpiValue}>{lastBill?.consumo_kwh || 0} kWh</Text>
            <Text style={styles.kpiLabel}>Consumo Atual</Text>
          </View>
          <View style={styles.kpiCard}>
            <Ionicons name="wallet" size={24} color="#2196F3" />
            <Text style={styles.kpiValue}>R$ {lastBill?.valor_total?.toFixed(2) || '0,00'}</Text>
            <Text style={styles.kpiLabel}>Última Conta</Text>
          </View>
          <View style={styles.kpiCard}>
            <Ionicons name="trending-up" size={24} color="#FF9800" />
            <Text style={styles.kpiValue}>{changePercent}%</Text>
            <Text style={styles.kpiLabel}>vs Mês Anterior</Text>
          </View>
        </View>

        {/* Gráfico */}
        <View style={styles.chartContainer}>
          <Text style={styles.sectionTitle}>Suas Contas</Text>
          {bills.length > 0 ? (
            <View style={styles.chart}>
              {bills.slice(0, 6).map((bill, index) => (
                <View key={bill.id} style={styles.chartBar}>
                  <View 
                    style={[
                      styles.bar, 
                      { 
                        height: Math.max((bill.consumo_kwh / Math.max(...bills.map(b => b.consumo_kwh))) * 100, 10),
                        backgroundColor: userColor
                      }
                    ]} 
                  />
                  <Text style={styles.barLabel}>{new Date(bill.period_start).getMonth() + 1}</Text>
                  <Text style={styles.barValue}>{bill.consumo_kwh}</Text>
                </View>
              ))}
            </View>
          ) : (
            <Text style={styles.noDataText}>Nenhuma conta cadastrada ainda</Text>
          )}
        </View>

        {/* Contas Recentes */}
        <View style={styles.billsContainer}>
          <Text style={styles.sectionTitle}>Contas Recentes</Text>
          {recentBills.length > 0 ? recentBills.map((bill) => (
            <View key={bill.id} style={styles.billCard}>
              <View style={styles.billInfo}>
                <Text style={styles.billDate}>{bill.period_start}</Text>
                <Text style={styles.billConsumption}>{bill.consumo_kwh} kWh</Text>
              </View>
              <View style={styles.billAmount}>
                <Text style={styles.billValue}>R$ {bill.valor_total.toFixed(2)}</Text>
                <View style={[styles.statusBadge, { backgroundColor: getStatusColor(bill.status) }]}>
                  <Text style={styles.statusText}>{bill.status}</Text>
                </View>
              </View>
            </View>
          )) : (
            <Text style={styles.noDataText}>Nenhuma conta cadastrada ainda</Text>
          )}
        </View>

        {/* Analytics */}
        {analytics && (
          <View style={styles.insightsContainer}>
            <Text style={styles.sectionTitle}>Resumo</Text>
            <View style={styles.insightCard}>
              <Ionicons name="document-text" size={24} color={userColor} />
              <View style={styles.insightText}>
                <Text style={styles.insightTitle}>Total de Contas</Text>
                <Text style={styles.insightDescription}>
                  {analytics.total_bills} contas processadas
                </Text>
              </View>
            </View>
            <View style={styles.insightCard}>
              <Ionicons name="flash" size={24} color="#FF9800" />
              <View style={styles.insightText}>
                <Text style={styles.insightTitle}>Consumo Total</Text>
                <Text style={styles.insightDescription}>
                  {analytics.total_consumption.toFixed(2)} kWh consumidos
                </Text>
              </View>
            </View>
            <View style={styles.insightCard}>
              <Ionicons name="wallet" size={24} color="#2196F3" />
              <View style={styles.insightText}>
                <Text style={styles.insightTitle}>Gasto Total</Text>
                <Text style={styles.insightDescription}>
                  R$ {analytics.total_cost.toFixed(2)} em contas
                </Text>
              </View>
            </View>
          </View>
        )}
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: theme.colors.background,
  },
  kpiContainer: {
    flexDirection: 'row',
    padding: 20,
    justifyContent: 'space-between',
  },
  kpiCard: {
    backgroundColor: theme.colors.surface,
    padding: 15,
    borderRadius: theme.borderRadius.md,
    alignItems: 'center',
    width: (width - 60) / 3,
    borderWidth: 1,
    borderColor: theme.colors.border,
  },
  kpiValue: {
    fontSize: 18,
    fontWeight: 'bold',
    color: theme.colors.text,
    marginTop: 5,
  },
  kpiLabel: {
    fontSize: 12,
    color: theme.colors.textSecondary,
    textAlign: 'center',
    marginTop: 5,
  },
  chartContainer: {
    backgroundColor: theme.colors.surface,
    margin: 20,
    padding: 20,
    borderRadius: theme.borderRadius.md,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: theme.colors.text,
    marginBottom: 15,
  },
  chart: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-end',
    height: 120,
  },
  chartBar: {
    alignItems: 'center',
    flex: 1,
  },
  bar: {
    width: 20,
    borderRadius: 2,
    marginBottom: 5,
  },
  barLabel: {
    fontSize: 12,
    color: theme.colors.textSecondary,
    marginTop: 5,
  },
  barValue: {
    fontSize: 10,
    color: theme.colors.textSecondary,
  },
  billsContainer: {
    backgroundColor: theme.colors.surface,
    margin: 20,
    padding: 20,
    borderRadius: theme.borderRadius.md,
  },
  billCard: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: 15,
    borderBottomWidth: 1,
    borderBottomColor: theme.colors.border,
  },
  billInfo: {
    flex: 1,
  },
  billDate: {
    fontSize: 16,
    fontWeight: '600',
    color: theme.colors.text,
  },
  billConsumption: {
    fontSize: 14,
    color: theme.colors.textSecondary,
    marginTop: 2,
  },
  billAmount: {
    alignItems: 'flex-end',
  },
  billValue: {
    fontSize: 16,
    fontWeight: 'bold',
    color: theme.colors.text,
  },
  statusBadge: {
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 12,
    marginTop: 4,
  },
  statusText: {
    fontSize: 12,
    color: 'white',
    fontWeight: '600',
  },
  insightsContainer: {
    backgroundColor: theme.colors.surface,
    margin: 20,
    padding: 20,
    borderRadius: theme.borderRadius.md,
  },
  insightCard: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    marginBottom: 15,
  },
  insightText: {
    flex: 1,
    marginLeft: 15,
  },
  insightTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: theme.colors.text,
    marginBottom: 5,
  },
  insightDescription: {
    fontSize: 14,
    color: theme.colors.textSecondary,
    lineHeight: 20,
  },
  noDataText: {
    textAlign: 'center',
    color: theme.colors.textSecondary,
    fontSize: 16,
    padding: 20,
  },
});

function getStatusColor(status: string): string {
  switch (status?.toLowerCase()) {
    case 'paid':
    case 'pago':
      return '#4CAF50';
    case 'pending':
    case 'pendente':
      return '#FF9800';
    case 'overdue':
    case 'vencido':
      return '#F44336';
    default:
      return '#999';
  }
}