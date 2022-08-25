def normalize_hashrate(coin, hashrate):
    if coin == 'bitcoin':
        # 1 × 10^10
        hashrate = float(hashrate) / 100000000000
        return int(hashrate)
    elif coin == 'ethereum':
        # 1 × 10^9
        return hashrate / 1000000000

