import { describe, it, expect, beforeEach, vi } from 'vitest';
import { mount } from '@vue/test-utils';
import AboutInfo from '../AboutInfo.vue';

// axios インスタンスのモックを作成
const axiosInstance = {
  get: vi.fn(() => Promise.resolve({ data: "message: 'dataデータ取得成功'" })),
  // 他の必要な axios メソッドをここに追加
};

vi.mock('axios', () => ({
  create: () => axiosInstance,
}));

describe('AboutInfo', () => {
	let wrapper;
	beforeEach(async () => {
		// モック化した axios インスタンスをコンポーネントに提供
		wrapper = await mount(AboutInfo, {
		global: {
			provide: {
			axios: axiosInstance,
			},
		},
		});
	});
  	it('axios: APIコール', async () => {
		expect(axiosInstance.get).toHaveBeenCalled();
		expect(wrapper.text()).toContain('dataデータ取得成功')
	});
	it('文言: タイトル', async () => {
		expect(wrapper.text()).toContain('About Info Page')
	});
});
