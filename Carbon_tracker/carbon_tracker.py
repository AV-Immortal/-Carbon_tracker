#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
低碳行为追踪系统
功能：
- 输入每日低碳行为数据（用电量、用水量、通勤方式）
- 计算单日/累计碳排放
- 保存数据到本地CSV文件
- 查看历史数据/碳排放趋势
"""

import csv
import os
from datetime import datetime
from typing import List, Dict, Optional


class CarbonTracker:
    """碳排放追踪器"""
    
    # 碳排放系数（单位：kg CO2）
    # 这些系数可以根据实际需求调整
    EMISSION_FACTORS = {
        'electricity': 0.581,  # 每度电的碳排放系数（kg CO2/kWh）
        'water': 0.001,         # 每吨水的碳排放系数（kg CO2/m³）
        'transport': {          # 通勤方式碳排放系数（kg CO2/km）
            '步行': 0.0,
            '自行车': 0.0,
            '地铁': 0.04,
            '公交': 0.089,
            '私家车': 0.192,
            '电动车': 0.053,
            '出租车': 0.192,
            '网约车': 0.192,
        }
    }
    
    def __init__(self, data_file: str = 'carbon_data.csv'):
        """初始化追踪器
        
        Args:
            data_file: CSV数据文件路径
        """
        self.data_file = data_file
        self.data: List[Dict] = []
        self._load_data()
    
    def _load_data(self) -> None:
        """从CSV文件加载数据"""
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                self.data = list(reader)
                # 转换数值类型
                for row in self.data:
                    row['electricity'] = float(row['electricity'])
                    row['water'] = float(row['water'])
                    row['distance'] = float(row['distance'])
                    row['carbon_emission'] = float(row['carbon_emission'])
        else:
            self.data = []
    
    def _save_data(self) -> None:
        """保存数据到CSV文件"""
        if not self.data:
            return
        
        fieldnames = ['date', 'electricity', 'water', 'transport', 'distance', 'carbon_emission']
        with open(self.data_file, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.data)
    
    def calculate_daily_emission(self, electricity: float, water: float, 
                                  transport: str, distance: float) -> float:
        """计算单日碳排放量
        
        Args:
            electricity: 用电量（kWh）
            water: 用水量（m³）
            transport: 通勤方式
            distance: 通勤距离（km）
        
        Returns:
            碳排放量（kg CO2）
        """
        # 用电碳排放
        electricity_emission = electricity * self.EMISSION_FACTORS['electricity']
        
        # 用水碳排放
        water_emission = water * self.EMISSION_FACTORS['water']
        
        # 通勤碳排放
        transport_emission = distance * self.EMISSION_FACTORS['transport'].get(
            transport, 0.192  # 默认使用私家车系数
        )
        
        total_emission = electricity_emission + water_emission + transport_emission
        return round(total_emission, 3)
    
    def add_record(self, date: str, electricity: float, water: float, 
                   transport: str, distance: float) -> bool:
        """添加一条记录
        
        Args:
            date: 日期（YYYY-MM-DD）
            electricity: 用电量（kWh）
            water: 用水量（m³）
            transport: 通勤方式
            distance: 通勤距离（km）
        
        Returns:
            是否成功添加
        """
        # 检查日期是否已存在
        if any(record['date'] == date for record in self.data):
            print(f"警告：日期 {date} 的数据已存在，如需修改请先删除原记录")
            return False
        
        # 计算碳排放
        carbon_emission = self.calculate_daily_emission(electricity, water, transport, distance)
        
        # 添加记录
        record = {
            'date': date,
            'electricity': electricity,
            'water': water,
            'transport': transport,
            'distance': distance,
            'carbon_emission': carbon_emission
        }
        self.data.append(record)
        
        # 按日期排序
        self.data.sort(key=lambda x: x['date'])
        
        # 保存到文件
        self._save_data()
        
        return True
    
    def get_daily_emission(self, date: str) -> Optional[float]:
        """获取指定日期的碳排放量
        
        Args:
            date: 日期（YYYY-MM-DD）
        
        Returns:
            碳排放量，如果不存在返回None
        """
        for record in self.data:
            if record['date'] == date:
                return record['carbon_emission']
        return None
    
    def get_total_emission(self, start_date: Optional[str] = None, 
                           end_date: Optional[str] = None) -> float:
        """获取累计碳排放量
        
        Args:
            start_date: 开始日期（YYYY-MM-DD），不指定则从最早记录开始
            end_date: 结束日期（YYYY-MM-DD），不指定则到最新记录结束
        
        Returns:
            累计碳排放量（kg CO2）
        """
        filtered_data = self.data
        
        if start_date:
            filtered_data = [r for r in filtered_data if r['date'] >= start_date]
        if end_date:
            filtered_data = [r for r in filtered_data if r['date'] <= end_date]
        
        total = sum(record['carbon_emission'] for record in filtered_data)
        return round(total, 3)
    
    def get_average_emission(self) -> float:
        """获取平均日碳排放量
        
        Returns:
            平均日碳排放量（kg CO2）
        """
        if not self.data:
            return 0.0
        total = sum(record['carbon_emission'] for record in self.data)
        return round(total / len(self.data), 3)
    
    def get_all_records(self) -> List[Dict]:
        """获取所有记录
        
        Returns:
            所有记录的列表
        """
        return self.data.copy()
    
    def get_records_by_date_range(self, start_date: str, end_date: str) -> List[Dict]:
        """获取指定日期范围内的记录
        
        Args:
            start_date: 开始日期（YYYY-MM-DD）
            end_date: 结束日期（YYYY-MM-DD）
        
        Returns:
            记录列表
        """
        return [r for r in self.data if start_date <= r['date'] <= end_date]
    
    def delete_record(self, date: str) -> bool:
        """删除指定日期的记录
        
        Args:
            date: 日期（YYYY-MM-DD）
        
        Returns:
            是否成功删除
        """
        original_length = len(self.data)
        self.data = [r for r in self.data if r['date'] != date]
        
        if len(self.data) < original_length:
            self._save_data()
            return True
        return False
    
    def get_trend(self, days: int = 7) -> List[Dict]:
        """获取最近N天的碳排放趋势
        
        Args:
            days: 天数
        
        Returns:
            最近N天的记录列表
        """
        if not self.data:
            return []
        return self.data[-days:] if len(self.data) >= days else self.data
    
    def get_transport_statistics(self) -> Dict[str, int]:
        """获取通勤方式统计
        
        Returns:
            各通勤方式的使用次数
        """
        stats = {}
        for record in self.data:
            transport = record['transport']
            stats[transport] = stats.get(transport, 0) + 1
        return stats


def print_menu():
    """打印主菜单"""
    print("\n" + "="*50)
    print("           低碳行为追踪系统")
    print("="*50)
    print("1. 添加每日数据")
    print("2. 查看单日碳排放")
    print("3. 查看累计碳排放")
    print("4. 查看所有历史数据")
    print("5. 查看碳排放趋势（最近7天）")
    print("6. 查看通勤方式统计")
    print("7. 删除记录")
    print("0. 退出")
    print("="*50)


def get_transport_methods() -> List[str]:
    """获取所有支持的通勤方式"""
    return list(CarbonTracker.EMISSION_FACTORS['transport'].keys())


def input_record() -> Dict:
    """输入一条记录
    
    Returns:
        包含记录数据的字典
    """
    print("\n--- 输入每日低碳行为数据 ---")
    
    # 输入日期
    while True:
        date_input = input("请输入日期（YYYY-MM-DD，留空使用今天）：").strip()
        if not date_input:
            date_str = datetime.now().strftime('%Y-%m-%d')
            break
        try:
            datetime.strptime(date_input, '%Y-%m-%d')
            date_str = date_input
            break
        except ValueError:
            print("日期格式错误，请使用 YYYY-MM-DD 格式")
    
    # 输入用电量
    while True:
        try:
            electricity = float(input("请输入用电量（kWh）："))
            if electricity < 0:
                print("用电量不能为负数")
                continue
            break
        except ValueError:
            print("请输入有效的数字")
    
    # 输入用水量
    while True:
        try:
            water = float(input("请输入用水量（m³）："))
            if water < 0:
                print("用水量不能为负数")
                continue
            break
        except ValueError:
            print("请输入有效的数字")
    
    # 输入通勤方式
    print("\n可选通勤方式：")
    methods = get_transport_methods()
    for i, method in enumerate(methods, 1):
        print(f"  {i}. {method}")
    
    while True:
        try:
            choice = int(input("请选择通勤方式（输入序号）："))
            if 1 <= choice <= len(methods):
                transport = methods[choice - 1]
                break
            print(f"请输入1-{len(methods)}之间的数字")
        except ValueError:
            print("请输入有效的数字")
    
    # 输入通勤距离
    while True:
        try:
            distance = float(input("请输入通勤距离（km）："))
            if distance < 0:
                print("通勤距离不能为负数")
                continue
            break
        except ValueError:
            print("请输入有效的数字")
    
    return {
        'date': date_str,
        'electricity': electricity,
        'water': water,
        'transport': transport,
        'distance': distance
    }


def display_record(record: Dict):
    """显示单条记录
    
    Args:
        record: 记录字典
    """
    print(f"\n日期: {record['date']}")
    print(f"用电量: {record['electricity']} kWh")
    print(f"用水量: {record['water']} m³")
    print(f"通勤方式: {record['transport']}")
    print(f"通勤距离: {record['distance']} km")
    print(f"碳排放量: {record['carbon_emission']} kg CO2")


def display_records(records: List[Dict]):
    """显示多条记录
    
    Args:
        records: 记录列表
    """
    if not records:
        print("\n暂无数据")
        return
    
    print("\n" + "-"*80)
    print(f"{'日期':<12} {'用电量':<10} {'用水量':<10} {'通勤方式':<10} {'距离':<10} {'碳排放':<12}")
    print("-"*80)
    
    for record in records:
        print(f"{record['date']:<12} {record['electricity']:<10.2f} "
              f"{record['water']:<10.2f} {record['transport']:<10} "
              f"{record['distance']:<10.2f} {record['carbon_emission']:<12.3f}")
    
    print("-"*80)


def display_trend(records: List[Dict]):
    """显示趋势分析
    
    Args:
        records: 记录列表
    """
    if not records:
        print("\n暂无数据")
        return
    
    print("\n--- 碳排放趋势分析 ---")
    
    # 计算趋势
    if len(records) >= 2:
        first = records[0]['carbon_emission']
        last = records[-1]['carbon_emission']
        change = last - first
        change_percent = (change / first) * 100 if first > 0 else 0
        
        if change > 0:
            trend = f"上升 {abs(change):.3f} kg CO2 ({abs(change_percent):.1f}%)"
        elif change < 0:
            trend = f"下降 {abs(change):.3f} kg CO2 ({abs(change_percent):.1f}%)"
        else:
            trend = "持平"
        
        print(f"趋势: {trend}")
    
    # 显示记录
    display_records(records)
    
    # 显示统计
    total = sum(r['carbon_emission'] for r in records)
    avg = total / len(records)
    max_emission = max(r['carbon_emission'] for r in records)
    min_emission = min(r['carbon_emission'] for r in records)
    
    print(f"\n统计信息:")
    print(f"  总排放: {total:.3f} kg CO2")
    print(f"  平均日排放: {avg:.3f} kg CO2")
    print(f"  最高日排放: {max_emission:.3f} kg CO2")
    print(f"  最低日排放: {min_emission:.3f} kg CO2")


def main():
    """主函数"""
    tracker = CarbonTracker()
    
    while True:
        print_menu()
        choice = input("\n请选择操作（0-7）：").strip()
        
        if choice == '0':
            print("\n感谢使用低碳行为追踪系统，再见！")
            break
        
        elif choice == '1':
            # 添加每日数据
            record = input_record()
            success = tracker.add_record(
                record['date'],
                record['electricity'],
                record['water'],
                record['transport'],
                record['distance']
            )
            
            if success:
                emission = tracker.get_daily_emission(record['date'])
                print(f"\n✓ 数据添加成功！")
                print(f"  日期: {record['date']}")
                print(f"  当日碳排放: {emission} kg CO2")
            else:
                print("\n✗ 数据添加失败")
        
        elif choice == '2':
            # 查看单日碳排放
            date = input("\n请输入日期（YYYY-MM-DD）：").strip()
            emission = tracker.get_daily_emission(date)
            
            if emission is not None:
                record = next(r for r in tracker.data if r['date'] == date)
                display_record(record)
            else:
                print(f"\n未找到日期 {date} 的数据")
        
        elif choice == '3':
            # 查看累计碳排放
            print("\n--- 查看累计碳排放 ---")
            start_date = input("请输入开始日期（YYYY-MM-DD，留空从最早记录开始）：").strip()
            end_date = input("请输入结束日期（YYYY-MM-DD，留空到最新记录结束）：").strip()
            
            start_date = start_date if start_date else None
            end_date = end_date if end_date else None
            
            total = tracker.get_total_emission(start_date, end_date)
            avg = tracker.get_average_emission()
            
            print(f"\n累计碳排放: {total} kg CO2")
            print(f"平均日碳排放: {avg} kg CO2")
            
            if start_date and end_date:
                records = tracker.get_records_by_date_range(start_date, end_date)
                print(f"统计天数: {len(records)} 天")
            else:
                print(f"统计天数: {len(tracker.data)} 天")
        
        elif choice == '4':
            # 查看所有历史数据
            records = tracker.get_all_records()
            display_records(records)
            
            if records:
                total = tracker.get_total_emission()
                print(f"\n总记录数: {len(records)} 条")
                print(f"累计碳排放: {total} kg CO2")
        
        elif choice == '5':
            # 查看碳排放趋势
            days_input = input("\n请输入查看天数（默认7天）：").strip()
            days = int(days_input) if days_input.isdigit() else 7
            
            records = tracker.get_trend(days)
            display_trend(records)
        
        elif choice == '6':
            # 查看通勤方式统计
            stats = tracker.get_transport_statistics()
            
            if not stats:
                print("\n暂无数据")
            else:
                print("\n--- 通勤方式统计 ---")
                print(f"{'通勤方式':<15} {'使用次数':<10} {'占比':<10}")
                print("-"*40)
                
                total = sum(stats.values())
                for transport, count in sorted(stats.items(), key=lambda x: x[1], reverse=True):
                    percent = (count / total) * 100
                    print(f"{transport:<15} {count:<10} {percent:.1f}%")
                
                print("-"*40)
                print(f"总记录: {total} 条")
        
        elif choice == '7':
            # 删除记录
            date = input("\n请输入要删除的日期（YYYY-MM-DD）：").strip()
            
            if tracker.delete_record(date):
                print(f"✓ 已删除日期 {date} 的记录")
            else:
                print(f"✗ 未找到日期 {date} 的记录")
        
        else:
            print("\n无效的选择，请重新输入")
        
        # 暂停，等待用户按键
        input("\n按回车键继续...")


if __name__ == '__main__':
    main()