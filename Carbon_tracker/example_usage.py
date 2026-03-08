#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
示例：如何使用 CarbonTracker 类进行编程式调用

这个文件展示了如何在自己的代码中使用 CarbonTracker 类
"""

from carbon_tracker import CarbonTracker


def example_basic_usage():
    """基础使用示例"""
    print("=" * 50)
    print("基础使用示例")
    print("=" * 50)
    
    # 创建追踪器实例
    tracker = CarbonTracker()
    
    # 添加一条记录
    success = tracker.add_record(
        date='2024-01-22',
        electricity=10.0,
        water=0.3,
        transport='地铁',
        distance=15.0
    )
    
    if success:
        print("✓ 记录添加成功")
    else:
        print("✗ 记录添加失败")
    
    # 查看单日碳排放
    emission = tracker.get_daily_emission('2024-01-22')
    print(f"2024-01-22 的碳排放: {emission} kg CO2")
    
    # 查看累计碳排放
    total = tracker.get_total_emission()
    print(f"累计碳排放: {total} kg CO2")
    
    print()


def example_date_range():
    """日期范围查询示例"""
    print("=" * 50)
    print("日期范围查询示例")
    print("=" * 50)
    
    tracker = CarbonTracker()
    
    # 查询指定日期范围内的记录
    records = tracker.get_records_by_date_range('2024-01-15', '2024-01-20')
    
    print(f"2024-01-15 到 2024-01-20 的记录:")
    for record in records:
        print(f"  {record['date']}: {record['carbon_emission']} kg CO2")
    
    # 计算该时间段的累计排放
    total = tracker.get_total_emission('2024-01-15', '2024-01-20')
    print(f"\n该时间段累计排放: {total} kg CO2")
    
    print()


def example_trend_analysis():
    """趋势分析示例"""
    print("=" * 50)
    print("趋势分析示例")
    print("=" * 50)
    
    tracker = CarbonTracker()
    
    # 获取最近7天的记录
    records = tracker.get_trend(days=7)
    
    if len(records) >= 2:
        first = records[0]['carbon_emission']
        last = records[-1]['carbon_emission']
        change = last - first
        
        print(f"最近7天趋势:")
        print(f"  首日排放: {first} kg CO2")
        print(f"  末日排放: {last} kg CO2")
        print(f"  变化: {change:+.3f} kg CO2")
        
        if change > 0:
            print("  趋势: 上升 ⬆️")
        elif change < 0:
            print("  趋势: 下降 ⬇️")
        else:
            print("  趋势: 持平 ➡️")
    
    print()


def example_statistics():
    """统计分析示例"""
    print("=" * 50)
    print("统计分析示例")
    print("=" * 50)
    
    tracker = CarbonTracker()
    
    # 平均排放量
    avg = tracker.get_average_emission()
    print(f"平均日排放: {avg} kg CO2")
    
    # 通勤方式统计
    stats = tracker.get_transport_statistics()
    print(f"\n通勤方式统计:")
    for transport, count in sorted(stats.items(), key=lambda x: x[1], reverse=True):
        print(f"  {transport}: {count} 次")
    
    print()


def example_batch_import():
    """批量导入示例"""
    print("=" * 50)
    print("批量导入示例")
    print("=" * 50)
    
    tracker = CarbonTracker()
    
    # 批量数据
    batch_data = [
        {'date': '2024-01-23', 'electricity': 9.5, 'water': 0.28, 'transport': '公交', 'distance': 12.0},
        {'date': '2024-01-24', 'electricity': 11.0, 'water': 0.30, 'transport': '地铁', 'distance': 15.0},
        {'date': '2024-01-25', 'electricity': 8.5, 'water': 0.25, 'transport': '自行车', 'distance': 5.0},
    ]
    
    print("批量导入数据:")
    for data in batch_data:
        success = tracker.add_record(
            data['date'],
            data['electricity'],
            data['water'],
            data['transport'],
            data['distance']
        )
        status = "✓" if success else "✗"
        print(f"  {status} {data['date']}")
    
    print()


def example_custom_calculation():
    """自定义计算示例"""
    print("=" * 50)
    print("自定义计算示例")
    print("=" * 50)
    
    tracker = CarbonTracker()
    
    # 直接使用计算方法
    emission = tracker.calculate_daily_emission(
        electricity=10.0,
        water=0.3,
        transport='地铁',
        distance=15.0
    )
    
    print(f"自定义计算结果: {emission} kg CO2")
    print(f"  用电: 10.0 kWh × 0.581 = {10.0 * 0.581:.3f} kg CO2")
    print(f"  用水: 0.3 m³ × 0.001 = {0.3 * 0.001:.3f} kg CO2")
    print(f"  通勤: 15.0 km × 0.04 = {15.0 * 0.04:.3f} kg CO2")
    print(f"  总计: {emission} kg CO2")
    
    print()


def example_export_to_list():
    """导出数据示例"""
    print("=" * 50)
    print("导出数据示例")
    print("=" * 50)
    
    tracker = CarbonTracker()
    
    # 获取所有记录
    all_records = tracker.get_all_records()
    
    print(f"总记录数: {len(all_records)}")
    print("\n前3条记录:")
    for record in all_records[:3]:
        print(f"  {record['date']}: {record['carbon_emission']} kg CO2")
    
    # 可以将数据导出为其他格式
    # 例如：导出为 JSON
    import json
    json_data = json.dumps(all_records, ensure_ascii=False, indent=2)
    print(f"\n导出为JSON格式（前100字符）:")
    print(json_data[:100] + "...")
    
    print()


def main():
    """运行所有示例"""
    print("\n" + "=" * 50)
    print("  CarbonTracker 类使用示例")
    print("=" * 50)
    print()
    
    try:
        example_basic_usage()
        example_date_range()
        example_trend_analysis()
        example_statistics()
        example_batch_import()
        example_custom_calculation()
        example_export_to_list()
        
        print("=" * 50)
        print("所有示例运行完成！")
        print("=" * 50)
        
    except Exception as e:
        print(f"运行示例时出错: {e}")


if __name__ == '__main__':
    main()