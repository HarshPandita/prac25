import java.util.*;

public class LongestSubstringNoRepeat {

    public int lengthOfLongestSubstring(String s) {
        Set<Character> seen = new HashSet<>();
        int left = 0, maxLength = 0;

        for (int right = 0; right < s.length(); right++) {
            char ch = s.charAt(right);
            while (seen.contains(ch)) {
                seen.remove(s.charAt(left));
                left++;
            }
            seen.add(ch);
            maxLength = Math.max(maxLength, right - left + 1);
        }

        return maxLength;
    }

    // Test it
    public static void main(String[] args) {
        LongestSubstringNoRepeat obj = new LongestSubstringNoRepeat();
        String s = "abcabcbb";
        System.out.println("Longest substring length: " + obj.lengthOfLongestSubstring(s)); // Output: 3
    }
}

// 

public class KokoEatingBananas {

    public int minEatingSpeed(int[] piles, int h) {
        int low = 1;
        int high = getMaxPile(piles);
        int result = high;

        while (low <= high) {
            int mid = low + (high - low) / 2;

            if (canEatAll(piles, h, mid)) {
                result = mid; // try smaller k
                high = mid - 1;
            } else {
                low = mid + 1; // need bigger k
            }
        }

        return result;
    }

    private boolean canEatAll(int[] piles, int h, int k) {
        int hours = 0;
        for (int pile : piles) {
            hours += (int) Math.ceil((double) pile / k);
        }
        return hours <= h;
    }

    private int getMaxPile(int[] piles) {
        int max = 0;
        for (int pile : piles) {
            max = Math.max(max, pile);
        }
        return max;
    }

    // Test it
    public static void main(String[] args) {
        KokoEatingBananas obj = new KokoEatingBananas();
        int[] piles = {3, 6, 7, 11};
        int h = 8;
        System.out.println("Minimum speed Koko needs: " + obj.minEatingSpeed(piles, h)); // Output: 4
    }
}