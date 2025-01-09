import { api } from 'src/boot/axios'

export const download = async (url, { autoRemove = true, filename = null } = {}) => {
  try {
    const { data, headers } = await api.get(url, { responseType: 'blob' })

    const href = URL.createObjectURL(data)

    const link = document.createElement('a')
    link.style.display = 'none'

    document.body.appendChild(link)

    const urlFilename = url?.split('/')?.at(-1) || ''

    const dispositionFilename = headers['content-disposition']?.split('filename=')?.[1]?.replace(/"/g, '') || ''

    link.setAttribute('href', href)
    link.setAttribute('download', filename || dispositionFilename || urlFilename)
    link.click()

    if (autoRemove) {
      document.body.removeChild(link)
      URL.revokeObjectURL(href)
      return
    }

    return link
  } catch (err) {}
}

export const preview = (url) => window.open(url, '_blank')
