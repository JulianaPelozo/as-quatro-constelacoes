// Marca provisória: quatro estrelas ligadas, como uma constelação.
// Trocar pelo logo oficial quando houver.
export default function Logo({ tamanho = 56 }) {
  return (
    <svg
      width={tamanho}
      height={tamanho}
      viewBox="0 0 64 64"
      aria-hidden="true"
      focusable="false"
    >
      <path
        d="M10 46 L25 22 L41 31 L54 12"
        fill="none"
        stroke="var(--link)"
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
        opacity="0.7"
      />
      <g fill="var(--destaque)">
        <circle cx="10" cy="46" r="4" />
        <circle cx="25" cy="22" r="4.5" />
        <circle cx="41" cy="31" r="3.5" />
        <circle cx="54" cy="12" r="5" />
      </g>
    </svg>
  )
}
